import asyncio
import aiohttp
import json
import logging
from aiohttp import web
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BackendServer:
    def __init__(self, url):
        self.url = url
        self.active = True
        self.failed_checks = 0

    def mark_active(self):
        if not self.active:
            logging.info(f"Backend {self.url} is now ACTIVE")
        self.active = True
        self.failed_checks = 0

    def mark_inactive(self):
        if self.active:
            logging.warning(f"Backend {self.url} is now INACTIVE")
        self.active = False
        self.failed_checks += 1

class BackendManager:
    def __init__(self, urls):
        self.servers = [BackendServer(url) for url in urls]
        self._index = 0
        self._lock = asyncio.Lock()

    def get_all_servers(self):
        return self.servers

    async def get_next_active_server(self):
        async with self._lock:
            start_index = self._index
            while True:
                server = self.servers[self._index]
                self._index = (self._index + 1) % len(self.servers)
                if server.active:
                    return server
                if self._index == start_index:
                    return None

async def check_backend(session, server, timeout_seconds, path):
    try:
        url = f"{server.url}{path}"
        timeout = aiohttp.ClientTimeout(total=timeout_seconds)
        async with session.get(url, timeout=timeout) as response:
            if response.status == 200:
                server.mark_active()
            else:
                server.mark_inactive()
    except (aiohttp.ClientError, asyncio.TimeoutError):
        server.mark_inactive()

async def health_checker(backend_manager, interval_seconds, timeout_seconds, path):
    logging.info("Starting health checker task...")
    async with aiohttp.ClientSession() as session:
        while True:
            servers = backend_manager.get_all_servers()
            tasks = [check_backend(session, server, timeout_seconds, path) for server in servers]
            await asyncio.gather(*tasks)
            await asyncio.sleep(interval_seconds)

class ProxyHandler:
    def __init__(self, backend_manager, max_concurrent_requests, max_retries, upstream_timeout_seconds):
        self.backend_manager = backend_manager
        self.max_retries = max_retries
        self.upstream_timeout_seconds = upstream_timeout_seconds
        self.semaphore = asyncio.Semaphore(max_concurrent_requests)
        self.client_session = None

    async def init_session(self):
        self.client_session = aiohttp.ClientSession()

    async def close_session(self):
        if self.client_session:
            await self.client_session.close()

    async def handle_request(self, request):
        async with self.semaphore:
            path = request.path_qs
            method = request.method
            headers = dict(request.headers)
            data = await request.read()

            for attempt in range(self.max_retries + 1):
                server = await self.backend_manager.get_next_active_server()
                if not server:
                    return web.Response(status=503, text="Service Unavailable: No active backends")

                target_url = f"{server.url}{path}"
                logging.info(f"Routing request to {target_url} (Attempt {attempt + 1})")

                try:
                    timeout = aiohttp.ClientTimeout(total=self.upstream_timeout_seconds)
                    async with self.client_session.request(
                        method, target_url, headers=headers, data=data, timeout=timeout
                    ) as response:
                        response_text = await response.read()
                        return web.Response(
                            body=response_text,
                            status=response.status,
                            headers=dict(response.headers)
                        )
                except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                    logging.warning(f"Failed to reach {target_url}: {e}")
                    server.mark_inactive()
                    if attempt == self.max_retries:
                        return web.Response(status=502, text="Bad Gateway")
                    
            return web.Response(status=502, text="Bad Gateway")

async def proxy_middleware(request):
    return await request.app['proxy_handler'].handle_request(request)

async def on_cleanup(app):
    await app['proxy_handler'].close_session()

async def start_app(config, host, port, backend_manager):
    app = web.Application()
    app['config'] = config
    proxy_config = config['proxy']
    
    proxy_handler = ProxyHandler(
        backend_manager=backend_manager,
        max_concurrent_requests=config['max_concurrent_requests'],
        max_retries=proxy_config['max_retries'],
        upstream_timeout_seconds=proxy_config['upstream_timeout_seconds']
    )
    await proxy_handler.init_session()
    app['proxy_handler'] = proxy_handler
    
    app.on_cleanup.append(on_cleanup)
    app.router.add_route('*', '/{tail:.*}', proxy_middleware)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host, port)
    await site.start()
    logging.info(f"Load Balancer listening on {host}:{port}")
    return runner

DEFAULT_CONFIG = {
    "backends": [
        "http://127.0.0.1:6001",
        "http://127.0.0.1:6002",
        "http://127.0.0.1:6003"
    ],
    "max_concurrent_requests": 500,
    "health_check": {
        "interval_seconds": 5,
        "timeout_seconds": 2,
        "path": "/health"
    },
    "proxy": {
        "max_retries": 2,
        "upstream_timeout_seconds": 3,
        "host": "0.0.0.0",
        "port": 5000
    }
}

async def run_servers():
    config = DEFAULT_CONFIG
    if os.path.exists('config.json'):
        with open('config.json', 'r') as f:
            config = json.load(f)

    backend_manager = BackendManager(config['backends'])
    hc_config = config['health_check']
    
    health_task = asyncio.create_task(
        health_checker(backend_manager, hc_config['interval_seconds'], hc_config['timeout_seconds'], hc_config['path'])
    )

    proxy_config = config['proxy']
    runner = await start_app(config, proxy_config['host'], proxy_config['port'], backend_manager)

    try:
        while True:
            await asyncio.sleep(3600)
    except asyncio.CancelledError:
        pass
    finally:
        health_task.cancel()
        await runner.cleanup()

def main():
    try:
        asyncio.run(run_servers())
    except KeyboardInterrupt:
        logging.info("Load Balancer stopped by user.")

if __name__ == '__main__':
    main()
