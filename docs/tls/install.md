## Auto Download

No additional steps are required! Simply use the Python syntax below, and the library will automatically detect and download the version compatible with your operating system by fetching it from the GitHub repository.

#### Reference: [GitHub Releases - TLS Client](https://github.com/bogdanfinn/tls-client/releases/)

The downloaded library files are stored in the `tls_requests/bin` directory.

```pycon
>>> from src import tls_requests
>>> r = tls_requests.get('https://httpbin.org/get')
```

## Manual Download

For manual installation, you can download the library using the following script:

```python
from tls_requests.models.libraries import TLSLibrary

TLSLibrary.load()
# OR: TLSLibrary.download()
```
