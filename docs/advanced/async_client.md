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
>>> import random
>>> import time
>>> import tls_requests
>>> async def fetch(idx, url):
    async with tls_requests.AsyncClient() as client:
        rand = random.uniform(0.1, 1.5)
        start_time = time.perf_counter()
        print("%s: Sleep for %.2f seconds." % (idx, rand))
        await asyncio.sleep(rand)
        response = await client.get(url)
        end_time = time.perf_counter()
        print("%s: Took: %.2f" % (idx, (end_time - start_time)))
        return response
>>> async def run(urls):
        tasks = [asyncio.create_task(fetch(idx, url)) for idx, url in enumerate(urls)]
        responses = await asyncio.gather(*tasks)
        return responses

>>> start_urls = [
    'https://httpbin.org/absolute-redirect/1',
    'https://httpbin.org/absolute-redirect/2',
    'https://httpbin.org/absolute-redirect/3',
    'https://httpbin.org/absolute-redirect/4',
    'https://httpbin.org/absolute-redirect/5',
]


>>> r = asyncio.run(run(start_urls))
>>> r
[<Response [200]>, <Response [200]>, <Response [200]>, <Response [200]>, <Response [200]>]

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
        response = await client.get("https://httpbin.org/get")
    finally:
        await client.aclose()
```

* * *

By using `AsyncClient`, you can unlock the full potential of asynchronous programming in Python while enjoying the simplicity and power of TLS Requests.
