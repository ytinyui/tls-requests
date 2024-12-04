Async Support in TLS Requests
=============================

TLS Requests provides support for asynchronous HTTP requests using the `AsyncClient`. This is especially useful when working in an asynchronous environment, such as with modern web frameworks, or when you need the performance benefits of asynchronous I/O.

* * *

Why Use Async?
--------------

*   **Improved Performance:** Async is more efficient than multi-threading for handling high concurrency workloads.
*   **Long-lived Connections:** Useful for protocols like WebSockets or long polling.
*   **Framework Compatibility:** Essential when integrating with async web frameworks (e.g., FastAPI, Starlette).

Advanced usage with syntax similar to Client, refer to the [Client documentation](client).

* * *

Making Async Requests
---------------------

To send asynchronous HTTP requests, use the `AsyncClient`:

```pycon
>>> import asyncio
>>> async def fetch(url):
        async with tls_requests.AsyncClient() as client:
            r = await client.get("https://www.example.com/")
            return r

>>> r = asyncio.run(fetch("https://httpbin.org/get"))
>>> r
<Response [200 OK]>
```

!!! tip
    Use [IPython](https://ipython.readthedocs.io/en/stable/) or Python 3.8+ with `python -m asyncio` to try this code interactively, as they support executing `async`/`await` expressions in the console.

* * *

Key API Differences
-------------------

When using `AsyncClient`, the API methods are asynchronous and must be awaited.

### Making Requests

Use `await` for all request methods:

*   `await client.get(url, ...)`
*   `await client.post(url, ...)`
*   `await client.put(url, ...)`
*   `await client.patch(url, ...)`
*   `await client.delete(url, ...)`
*   `await client.options(url, ...)`
*   `await client.head(url, ...)`
*   `await client.request(method, url, ...)`
*   `await client.send(request, ...)`

* * *

### Managing Client Lifecycle

#### Context Manager

For proper resource cleanup, use `async with`:

```python
import asyncio

async def fetch(url):
    async with tls_requests.AsyncClient() as client:
        response = await client.get(url)
        return response

r = asyncio.run(fetch("https://httpbin.org/get"))
print(r)  # <Response [200 OK]>
```

#### Manual Closing

Alternatively, explicitly close the client:

```python
import asyncio

async def fetch(url):
    client = tls_requests.AsyncClient()
    try:
        response = await client.get("https://www.example.com/")
    finally:
        await client.aclose()
```

* * *

By using `AsyncClient`, you can unlock the full potential of asynchronous programming in Python while enjoying the simplicity and power of TLS Requests.
