# Authentication

This section covers how to use authentication in your requests with `tls_requests`, offering both built-in options and the flexibility to define custom mechanisms.

* * *

Basic Authentication
--------------------

### Using a Tuple (Username and Password)

For basic HTTP authentication, pass a tuple `(username, password)` when initializing a `Client`.
This will automatically include the credentials in the `Authorization` header for all outgoing requests:


```pycon
>>> client = tls_requests.Client(auth=("username", "secret"))
>>> response = client.get("https://www.example.com/")
```

* * *

### Using a Custom Function

To customize how authentication is handled, you can use a function that modifies the request directly:

```pycon
>>> def custom_auth(request):
        request.headers["X-Authorization"] = "123456"
        return request

>>> client = tls_requests.Client(auth=custom_auth)
>>> response = client.get("https://www.example.com/")
>>> response
<Response [200 OK]>
```

* * *

Custom Authentication
---------------------

For advanced use cases, you can define custom authentication schemes by subclassing `tls_requests.Auth` and overriding the `build_auth` method.

### Bearer Token Authentication

This example demonstrates how to implement Bearer token-based authentication by adding an `Authorization` header:


```python
class BearerAuth(tls_requests.Auth):
    def __init__(self, token):
        self.token = token

    def build_auth(self, request: tls_requests.Request) -> tls_requests.Request | None:
        request.headers['Authorization'] = f"Bearer {self.token}"
        return request
```

* * *

### Usage Example

To use your custom `BearerAuth` implementation:

```pycon
>>> auth = BearerAuth(token="your_jwt_token")
>>> client = tls_requests.Client(auth=auth)
>>> response = client.get("https://www.example.com/secure-endpoint")
>>> response
<Response [200 OK]>
```

With these approaches, you can integrate various authentication strategies into your `tls_requests` workflow, whether built-in or custom-designed for specific needs.
