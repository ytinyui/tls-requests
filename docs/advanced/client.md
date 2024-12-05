Client Usage
================================

This guide details how to utilize the `tls_requests.Client` for efficient and advanced HTTP networking.
If you're transitioning from the popular `requests` library, the `Client` in `tls_requests` provides a powerful alternative with enhanced capabilities.

* * *

Why Use a Client?
-----------------

!!! hint
    If you’re familiar with `requests`, think of `tls_requests.Client()` as the equivalent of `requests.Session()`.

### TL;DR

Use a `Client` instance if you're doing more than one-off scripts or prototypes. It optimizes network resource usage by reusing connections, which is critical for performance when making multiple requests.

**Advantages:**

*   Efficient connection reuse.
*   Simplified configuration sharing across requests.
*   Advanced control over request behavior and customization.

* * *

Recommended Usage
-----------------

### Using a Context Manager

The best practice is to use a `Client` as a context manager. This ensures connections are properly cleaned up:

```python
with tls_requests.Client() as client:
    response = client.get("https://httpbin.org/get")
    print(response)  # <Response [200 OK]>
```

### Explicit Cleanup

If not using a context manager, ensure to close the client explicitly:

```python
client = tls_requests.Client()
try:
    response = client.get("https://httpbin.org/get")
    print(response)  # <Response [200 OK]>
finally:
    client.close()
```

* * *

Making Requests
---------------

A `Client` can send requests using methods like `.get()`, `.post()`, etc.:

```python
with tls_requests.Client() as client:
    response = client.get("https://httpbin.org/get")
    print(response)  # <Response [200 OK]>
```

### Custom Headers

To include custom headers in a request:

```python
headers = {'X-Custom': 'value'}
with tls_requests.Client() as client:
    response = client.get("https://httpbin.org/get", headers=headers)
    print(response.request.headers['X-Custom'])  # 'value'
```

* * *

Sharing Configuration Across Requests
-------------------------------------

You can apply default configurations, such as headers, for all requests made with the `Client`:

```python
headers = {'user-agent': 'my-app/1.0'}
with tls_requests.Client(headers=headers) as client:
    response = client.get("https://httpbin.org/headers")
    print(response.json()['headers']['User-Agent'])  # 'my-app/1.0'
```

* * *

Merging Configurations
----------------------

When client-level and request-level options overlap:

*   **Headers, query parameters, cookies:** Combined. Example:

```python
client_headers = {'X-Auth': 'client'}
request_headers = {'X-Custom': 'request'}
with tls_requests.Client(headers=client_headers) as client:
    response = client.get("https://httpbin.org/get", headers=request_headers)
    print(response.request.headers['X-Auth'])  # 'client'
    print(response.request.headers['X-Custom'])  # 'request'
```

*   **Other parameters:** Request-level options take precedence.

```python
with tls_requests.Client(auth=('user', 'pass')) as client:
    response = client.get("https://httpbin.org/get", auth=('admin', 'adminpass'))
    print(response.request.headers['Authorization'])  # Encoded 'admin:adminpass'

```

* * *

Advanced Request Handling
-------------------------

For more control, explicitly build and send `Request` instances:

```python
request = tls_requests.Request("GET", "https://httpbin.org/get")
with tls_requests.Client() as client:
    response = client.send(request)
    print(response)  # <Response [200 OK]>
```

To combine client- and request-level configurations:

```python
with tls_requests.Client(headers={"X-Client-ID": "ABC123"}) as client:
    request = client.build_request("GET", "https://httpbin.org/json")
    del request.headers["X-Client-ID"]  # Modify as needed
    response = client.send(request)
    print(response)
```

* * *

File Uploads
------------

Upload files with control over file name, content, and MIME type:

```python
files = {'upload-file': (None, 'text content', 'text/plain')}
response = tls_requests.post("https://httpbin.org/post", files=files)
print(response.json()['form']['upload-file'])  # 'text content'
```

For further details, refer to the library's documentation.
