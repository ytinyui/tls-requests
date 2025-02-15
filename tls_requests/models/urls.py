from __future__ import annotations

from abc import ABC
from collections.abc import Mapping
from typing import Any, ItemsView, KeysView, Union, ValuesView
from urllib.parse import ParseResult, quote, unquote, urlencode, urlparse

import idna

from tls_requests.exceptions import ProxyError, URLError, URLParamsError
from tls_requests.types import (URL_ALLOWED_PARAMS, ProxyTypes, URLParamTypes,
                                URLTypes)

__all__ = ["URL", "URLParams", "Proxy"]


class URLParams(Mapping, ABC):
    """URLParams

    Represents a mapping of URL parameters with utilities for normalization, encoding, and updating.
    This class provides a dictionary-like interface for managing URL parameters, ensuring that keys
    and values are properly validated and normalized.

    Attributes:
        - params (str): Returns the encoded URL parameters as a query string.

    Methods:
        - update(params: URLParamTypes = None, **kwargs): Updates the current parameters with new ones.
        - keys() -> KeysView: Returns a view of the parameter keys.
        - values() -> ValuesView: Returns a view of the parameter values.
        - items() -> ItemsView: Returns a view of the parameter key-value pairs.
        - copy() -> URLParams: Returns a copy of the current instance.
        - normalize(s: URL_ALLOWED_PARAMS): Normalizes a key or value to a string.

    Raises:
        - URLParamsError: Raised for invalid keys, values, or parameter types during initialization or updates.

    Example Usage:
        >>> params = URLParams({'key1': 'value1', 'key2': ['value2', 'value3']})
        >>> print(str(params))
        'key1=value1&key2=value2&key2=value3'

        >>> params.update({'key3': 'value4'})
        >>> print(params)
        'key1=value1&key2=value2&key2=value3&key3=value4'

        >>> 'key1' in params
        True
    """

    def __init__(self, params: URLParamTypes = None, **kwargs):
        self._data = self._prepare(params, **kwargs)

    @property
    def params(self) -> str:
        return str(self)

    def update(self, params: URLParamTypes = None, **kwargs):
        self._data.update(self._prepare(params, **kwargs))
        return self

    def keys(self) -> KeysView:
        return self._data.keys()

    def values(self) -> ValuesView:
        return self._data.values()

    def items(self) -> ItemsView:
        return self._data.items()

    def copy(self) -> URLParams:
        return self.__class__(self._data.copy())

    def __str__(self):
        return urlencode(self._data, doseq=True)

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.items())

    def __contains__(self, key: Any) -> bool:
        return key in self._data

    def __setitem__(self, key, value):
        self._data.update(self._prepare({key: value}))

    def __getitem__(self, key):
        return self._data[key]

    def __delitem__(self, key):
        del self._data[key]

    def __iter__(self):
        return (k for k in self.keys())

    def __len__(self) -> int:
        return len(self._data)

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            if isinstance(other, Mapping):
                other = self.__class__(other)
            else:
                return False
        return bool(self.params == other.params)

    def _prepare(self, params: URLParamTypes = None, **kwargs) -> Mapping:
        params = params or {}
        if not isinstance(params, (dict, self.__class__)):
            raise URLParamsError("Invalid parameters.")

        params.update(kwargs)
        for k, v in params.items():
            if not isinstance(k, (str, bytes)):
                raise URLParamsError("Invalid parameters key type.")

            if isinstance(v, (list, tuple, set)):
                v = [self.normalize(s) for s in v]
            else:
                v = self.normalize(v)

            params[self.normalize(k)] = v
        return params

    def normalize(self, s: URL_ALLOWED_PARAMS):
        if not isinstance(s, (str, bytes, int, float, bool)):
            raise URLParamsError("Invalid parameters value type.")

        if isinstance(s, bool):
            return str(s).lower()

        if isinstance(s, bytes):
            return s.decode("utf-8")

        return str(s)


class URL:
    """URL

    A utility class for parsing, manipulating, and constructing URLs. It integrates with the
    `URLParams` class for managing query parameters and provides easy access to various components
    of a URL, such as scheme, host, port, and path.

    Attributes:
        - url (str): The raw or prepared URL string.
        - params (URLParams): An instance of URLParams to manage query parameters.
        - parsed (ParseResult): A `ParseResult` object containing the parsed components of the URL.
        - auth (tuple): A tuple of (username, password) extracted from the URL.
        - fragment (str): The fragment identifier of the URL.
        - host (str): The hostname (IDNA-encoded if applicable).
        - path (str): The path component of the URL.
        - netloc (str): The network location (host:port if port is present).
        - password (str): The password extracted from the URL.
        - port (str): The port number of the URL.
        - query (str): The query string, incorporating both existing and additional parameters.
        - scheme (str): The URL scheme (e.g., "http", "https").
        - username (str): The username extracted from the URL.

    Methods:
        - _prepare(url: Union[U, str, bytes]) -> str: Prepares and validates a URL string or bytes to ParseResult.
        - _build(secure: bool = False) -> str: Constructs a URL string from its components.

    Raises:
        - URLError: Raised when an invalid URL or component is encountered.

    Example Usage:
        >>> url = URL("https://example.com/path?q=1#fragment", params={"key": "value"})
        >>> print(url.scheme)
        'https'
        >>> print(url.host)
        'example.com'
        >>> print(url.query)
        'q%3D1&key%3Dvalue'
        >>> print(url.params)
        'key=value'
        >>> url.params.update({'key2': 'value2'})
        >>> print(url.url)
        'https://example.com/path?q%3D1&key%3Dvalue%26key2%3Dvalue2#fragment'
        >>> from urllib.parse import unquote
        >>> print(unquote(url.url))
        'https://example.com/path?q=1&key=value&key2=value2#fragment'
        >>> url.url = 'https://example.org/'
        >>> print(unquote(url.url))
        'https://example.org/?key=value&key2=value2'
        >>> url.url = 'https://httpbin.org/get'
        >>> print(unquote(url.url))
        'https://httpbin.org/get?key=value&key2=value2'
    """

    __attrs__ = (
        "auth",
        "scheme",
        "host",
        "port",
        "path",
        "fragment",
        "username",
        "password",
    )

    def __init__(self, url: URLTypes, params: URLParamTypes = None, **kwargs):
        self._parsed = self._prepare(url)
        self._url = None
        self._params = URLParams(params)

    @property
    def url(self):
        if self._url is None:
            self._url = self._build(False)
        return self._url

    @url.setter
    def url(self, value):
        self._parsed = self._prepare(value)
        self._url = self._build(False)

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, value):
        self._url = None
        self._params = URLParams(value)

    @property
    def parsed(self) -> ParseResult:
        return self._parsed

    @property
    def netloc(self) -> str:
        return ":".join([self.host, self.port]) if self.port else self.host

    @property
    def query(self) -> str:
        query = ""
        if self.parsed.query and self.params.params:
            query = "&".join([quote(self.parsed.query), self.params.params])
        elif self.params.params:
            query = self.params.params
        elif self.parsed.query:
            query = self.parsed.query
        return query

    def __str__(self):
        return self._build()

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, unquote(self._build(True)))

    def _prepare(self, url: Union[T, str, bytes]) -> ParseResult:
        if isinstance(url, bytes):
            url = url.decode("utf-8")
        elif isinstance(url, self.__class__) or issubclass(
            self.__class__, url.__class__
        ):
            url = str(url)

        if not isinstance(url, str):
            raise URLError("Invalid URL: %s" % url)

        for attr in self.__attrs__:
            setattr(self, attr, None)

        parsed = urlparse(url.lstrip())

        self.auth = parsed.username, parsed.password
        self.scheme = parsed.scheme

        try:
            self.host = idna.encode(parsed.hostname.lower()).decode("ascii")
        except AttributeError:
            self.host = ""
        except idna.IDNAError:
            raise URLError("Invalid IDNA hostname.")

        self.port = ""
        try:
            if parsed.port:
                self.port = str(parsed.port)
        except ValueError as e:
            raise URLError("%s. port range must be 0 - 65535." % e.args[0])

        self.path = parsed.path
        self.fragment = parsed.fragment
        self.username = parsed.username or ""
        self.password = parsed.password or ""
        return parsed

    def _build(self, secure: bool = False) -> str:
        urls = [self.scheme, "://"]
        authority = self.netloc
        if self.username or self.password:
            password = self.password or ""
            if secure:
                password = "[secure]"

            authority = "@".join(
                [
                    ":".join([self.username, password]),
                    self.netloc,
                ]
            )

        urls.append(authority)
        if self.query:
            urls.append("?".join([self.path, self.query]))
        else:
            urls.append(self.path)

        if self.fragment:
            urls.append("#" + self.fragment)

        return "".join(urls)


class Proxy(URL):
    """Proxy

    A specialized subclass of `URL` designed to handle proxy URLs with specific schemes and additional
    validations. The class restricts allowed schemes to "http", "https", "socks5", and "socks5h". It
    also modifies the URL construction process to focus on proxy-specific requirements.

    Attributes:
        - ALLOWED_SCHEMES (tuple): A tuple of allowed schemes for the proxy ("http", "https", "socks5", "socks5h").
    Raises:
        - ProxyError: Raised when an invalid proxy or unsupported protocol is encountered.

    Example Usage:
        >>> proxy = Proxy("http://user:pass@127.0.0.1:8080")
        >>> print(proxy.scheme)
        'http'
        >>> print(proxy.netloc)
        '127.0.0.1:8080'
        >>> print(proxy)
        'http://user:pass@127.0.0.1:8080'
        >>> print(proxy.__repr__())
        '<Proxy: http://[secure]@127.0.0.1:8080>'

        >>> socks5 = Proxy("socks5://127.0.0.1:8080")
        >>> print(socks)
        'socks5://127.0.0.1:8080'
    """

    ALLOWED_SCHEMES = ("http", "https", "socks5", "socks5h")

    def _prepare(self, url: ProxyTypes) -> ParseResult:
        try:
            if isinstance(url, bytes):
                url = url.decode("utf-8")

            if isinstance(url, str):
                url = url.strip()

            parsed = super(Proxy, self)._prepare(url)
            if str(parsed.scheme).lower() not in self.ALLOWED_SCHEMES:
                raise ProxyError(
                    "Invalid proxy scheme `%s`. The allowed schemes are ('http', 'https', 'socks5', 'socks5h')."
                    % parsed.scheme
                )

            return urlparse("%s://%s" % (parsed.scheme, parsed.netloc))
        except URLError:
            raise ProxyError("Invalid proxy: %s" % url)

    def _build(self, secure: bool = False) -> str:
        urls = [self.scheme, "://"]
        authority = self.netloc
        if self.username or self.password:
            userinfo = ":".join([self.username, self.password])
            if secure:
                userinfo = "[secure]"

            authority = "@".join(
                [
                    userinfo,
                    self.netloc,
                ]
            )

        urls.append(authority)
        return "".join(urls)
