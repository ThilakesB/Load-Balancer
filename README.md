<div align="center">
  <a href="#">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://via.placeholder.com/600x150/000000/FFFFFF?text=Python+Load+Balancer">
      <source media="(prefers-color-scheme: light)" srcset="https://via.placeholder.com/600x150/FFFFFF/000000?text=Python+Load+Balancer">
      <img alt="Python Load Balancer Logo" src="https://via.placeholder.com/600x150/FFFFFF/000000?text=Python+Load+Balancer" width="50%">
    </picture>
  </a>
</div>

<div align="center">
  <h3>High-performance, asynchronous HTTP orchestration framework for routing web traffic.</h3>
</div>

<div align="center">
  <a href="https://opensource.org/licenses/MIT" target="_blank"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License"></a>
  <a href="#" target="_blank"><img src="https://img.shields.io/badge/Python-3.8%2B-blue.svg" alt="Python Version"></a>
  <a href="#" target="_blank"><img src="https://img.shields.io/badge/aiohttp-supported-brightgreen.svg" alt="aiohttp Framework"></a>
  <a href="#" target="_blank"><img src="https://img.shields.io/badge/Status-Active-success.svg" alt="Status"></a>
</div>

<br>

Designed for robust web applications – the Python Load Balancer is a high-performance orchestration framework for distributing, managing, and health-checking incoming HTTP traffic asynchronously.

```bash
pip install -r requirements.txt
```

If you're looking to quickly test out the load balancer, check out the provided `test_backends.py` to easily spin up mock servers.

> [!NOTE]
> Ensure you have activated your virtual environment before running the load balancer.

## Why use Python Load Balancer?

This Load Balancer provides low-level supporting infrastructure for *any* high-volume, scalable web application:

- **Durable routing** — Distributes incoming HTTP requests sequentially (Round-Robin) across all active backends to ensure even load distribution.
- **Active health-checks** — Actively monitors the health of backend servers and automatically marks them as inactive if they fail to respond, seamlessly pulling them out of the rotation.
- **Resilient retries** — Automatically retries failed requests on the next available backend server to ensure high availability and prevent dropped connections.
- **High concurrency** — Handles a massive volume of concurrent requests efficiently without blocking, using Python's native asynchronous I/O (`aiohttp`).
- **Production-ready configuration** — Easily adjust settings like upstream timeouts, retry limits, and concurrent caps via a lightweight `config.json` file.

## Usage Guide

While this Load Balancer can be used standalone, it is designed to integrate seamlessly with your existing backend architectures.

### 1. Configure the Load Balancer

Edit the `config.json` file to customize the load balancer settings:
- `backends`: List of backend server URLs.
- `max_concurrent_requests`: Maximum number of concurrent requests the load balancer will handle.
- `health_check`: Settings for active health checking (`interval_seconds`, `timeout_seconds`, `path`).
- `proxy`: Settings for the proxy logic (`max_retries`, `upstream_timeout_seconds`, `port`, `host`).

### 2. Start the Backend Servers (Testing)

You can run the provided `test_backends.py` script to simulate multiple backend servers running on ports `6001`, `6002`, and `6003`:

```bash
python test_backends.py
```
*Leave this running in one terminal window.*

### 3. Start the Load Balancer

Open a **new terminal window**, activate the virtual environment, and run the load balancer:

```bash
.\venv\Scripts\Activate.ps1
python loadbalancer.py
```

### 4. Test the Load Balancer

With both the backends and the load balancer running, you can send requests to the load balancer:

```bash
curl http://127.0.0.1:5000/
```

You will receive responses alternating between the backend servers, demonstrating the round-robin routing in action.
