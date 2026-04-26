import asyncio
from aiohttp import web
import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

async def handle(request):
    port = request.app['port']
    text = f"Hello from backend running on port {port}!\n"
    return web.Response(text=text)

async def health(request):
    return web.Response(text="OK")

async def start_server(port):
    app = web.Application()
    app['port'] = port
    app.router.add_route('GET', '/health', health)
    app.router.add_route('*', '/{tail:.*}', handle)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '127.0.0.1', port)
    await site.start()
    logging.info(f"Backend started on http://127.0.0.1:{port}")
    return runner

async def main():
    ports = [6001, 6002, 6003]
    if len(sys.argv) > 1:
        ports = [int(p) for p in sys.argv[1:]]

    runners = []
    for port in ports:
        runner = await start_server(port)
        runners.append(runner)

    try:
        while True:
            await asyncio.sleep(3600)
    except KeyboardInterrupt:
        pass
    finally:
        for runner in runners:
            await runner.cleanup()

if __name__ == '__main__':
    asyncio.run(main())
