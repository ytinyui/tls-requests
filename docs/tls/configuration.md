To use custom TLS Client configuration follow these instructions:


### Default TLS Config
The `TLSConfig` class provides a structured and flexible way to configure TLS-specific settings for HTTP requests.
It supports features like custom headers, cookie handling, proxy configuration, and advanced TLS options.

Example:
    Initialize a `TLSConfig` object using predefined or default settings:

```pycon
>>> import tls_requests
>>> kwargs = {
    "catchPanics": false,
    "certificatePinningHosts": {},
    "customTlsClient": {},
    "followRedirects": false,
    "forceHttp1": false,
    "headerOrder": [
        "accept",
        "user-agent",
        "accept-encoding",
        "accept-language"
    ],
    "headers": {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7"
    },
    "insecureSkipVerify": false,
    "isByteRequest": false,
    "isRotatingProxy": false,
    "proxyUrl": "",
    "requestBody": "",
    "requestCookies": [
        {
            "_name": "foo",
            "value": "bar",
        },
        {
            "_name": "bar",
            "value": "foo",
        },
    ],
    "requestMethod": "GET",
    "requestUrl": "https://microsoft.com",
    "sessionId": "2my-session-id",
    "timeoutSeconds": 30,
    "tlsClientIdentifier": "chrome_120",
    "withDebug": false,
    "withDefaultCookieJar": false,
    "withRandomTLSExtensionOrder": false,
    "withoutCookieJar": false
}
>>> obj = tls_requests.tls.TLSConfig.from_kwargs(**kwargs)
>>> config_kwargs = obj.to_dict()
>>> r = tls_requests.get("https://httpbin.org/get", **config_kwargs)
>>> r
<Response [200 OK]>
```

### Custom TLS Client Configuration

The `CustomTLSClientConfig` class defines advanced configuration options for customizing TLS client behavior.
It includes support for ALPN, ALPS protocols, certificate compression, HTTP/2 settings, JA3 fingerprints, and
other TLS-related settings.

Example:
    Create a `CustomTLSClientConfig` instance with specific settings:

```pycon
>>> import tls_requests
>>> kwargs = {
    "alpnProtocols": [
        "h2",
        "http/1.1"
    ],
    "alpsProtocols": [
        "h2"
    ],
    "certCompressionAlgo": "brotli",
    "connectionFlow": 15663105,
    "h2Settings": {
        "HEADER_TABLE_SIZE": 65536,
        "MAX_CONCURRENT_STREAMS": 1000,
        "INITIAL_WINDOW_SIZE": 6291456,
        "MAX_HEADER_LIST_SIZE": 262144
    },
    "h2SettingsOrder": [
        "HEADER_TABLE_SIZE",
        "MAX_CONCURRENT_STREAMS",
        "INITIAL_WINDOW_SIZE",
        "MAX_HEADER_LIST_SIZE"
    ],
    "headerPriority": null,
    "ja3String": "771,2570-4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53,2570-0-23-65281-10-11-35-16-5-13-18-51-45-43-27-17513-2570-21,2570-29-23-24,0",
    "keyShareCurves": [
        "GREASE",
        "X25519"
    ],
    "priorityFrames": [],
    "pseudoHeaderOrder": [
        ":method",
        ":authority",
        ":scheme",
        ":path"
    ],
    "supportedSignatureAlgorithms": [
        "ECDSAWithP256AndSHA256",
        "PSSWithSHA256",
        "PKCS1WithSHA256",
        "ECDSAWithP384AndSHA384",
        "PSSWithSHA384",
        "PKCS1WithSHA384",
        "PSSWithSHA512",
        "PKCS1WithSHA512"
    ],
    "supportedVersions": [
        "GREASE",
        "1.3",
        "1.2"
    ]
}
>>> custom_tls_client = tls_requests.tls.CustomTLSClientConfig.from_kwargs(**kwargs)
>>> config_obj = tls_requests.tls.TLSConfig(customTlsClient=custom_tls_client, tlsClientIdentifier=None)
>>> config_kwargs = config_obj.to_dict()
>>> r = tls_requests.get("https://httpbin.org/get", **config_kwargs)
>>> r
<Response [200 OK]>
```

!!! note
    When using `CustomTLSClientConfig`, the `tlsClientIdentifier` parameter in TLSConfig is set to None.

### Passing Request Parameters Directly

```pycon
>>> import tls_requests
>>> r = tls_requests.get(
        url = "https://httpbin.org/get",
        proxy = "https://abc:123456@127.0.0.1:8080",
        http2 = True,
        timeout = 10.0,
        follow_redirects = True,
        verify = True,
        tls_identifier = "chrome_120",
        **config,
    )
>>> r
<Response [200 OK]>
```

!!! note
    When using the `customTlsClient` parameter within `**config`, the `tls_identifier` parameter will not be set.
    Parameters such as `headers`, `cookies`, `proxy`, `timeout`, `verify`, and `tls_identifier` will override the existing configuration in TLSConfig.

### `Client` and `AsyncClient` Parameters
```pycon
>>> import tls_requests
>>> client = tls_requests.Client(
        proxy = "https://abc:123456@127.0.0.1:8080",
        http2 = True,
        timeout = 10.0,
        follow_redirects = True,
        verify = True,
        tls_identifier = "chrome_120",
        **config,
    )
>>> r = client.get(url = "https://httpbin.org/get",)
>>> r
<Response [200 OK]>

```

!!! note
    The `Client` and `AsyncClient` interfaces in `tls_requests` enable reusable and shared configurations for multiple requests, providing a more convenient and efficient approach for handling HTTP requests.
