Using Proxies
================================

The `tls_requests` library supports HTTP and SOCKS proxies for routing traffic through an intermediary server.
This guide explains how to configure proxies for your client or individual requests.

* * *

How Proxies Work
-----------------

Proxies act as intermediaries between your client and the target server, handling requests and responses on your behalf. They can provide features like anonymity, filtering, or traffic logging.

* * *

### HTTP Proxies

To route traffic through an HTTP proxy, specify the proxy URL in the `proxy` parameter during client initialization:

```python
with tls_requests.Client(proxy="http://localhost:8030") as client:
    response = client.get("https://example.com")
    print(response)  # <Response [200 OK]>

```

### SOCKS Proxies

For SOCKS proxies, use the `socks5` scheme in the proxy URL:

```python
client = tls_requests.Client(proxy="socks5://user:pass@host:port")
response = client.get("https://example.com")
print(response)  # <Response [200 OK]>
```

### Supported Protocols:
*   **HTTP**: Use the `http://` scheme.
*   **HTTPS**: Use the `https://` scheme.
*   **SOCKS5**: Use the `socks5://` scheme.

* * *

### Proxy Authentication

You can include proxy credentials in the `userinfo` section of the URL:

```python
with tls_requests.Client(proxy="http://username:password@localhost:8030") as client:
    response = client.get("https://example.com")
    print(response)  # <Response [200 OK]>
```

Key Notes:
----------

*   **HTTPS Support**: Both HTTP and SOCKS proxies work for HTTPS requests.
*   **Performance**: Using a proxy may slightly impact performance due to the additional routing layer.
*   **Security**: Ensure proxy credentials and configurations are handled securely to prevent data leaks.
