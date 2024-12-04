Default TLS Configuration
---------------------

When initializing a `Client` or `AsyncClient`, a `TLSClient` instance is created with the following default settings:

*   **Timeout:** 30 seconds.
*   **Profile:** Chrome 120.
*   **Random TLS Extension Order:** Enabled.
*   **Redirects:** Always `False`.
*   **Idle Connection Closure:** After 90 seconds.
*   **Session ID:** Auto generate V4 UUID string if set to None.
*   **Force HTTP/1.1:** Default `False`.

All requests use [`Bogdanfinn's TLS-Client`](https://github.com/bogdanfinn/tls-client) to spoof the TLS client fingerprint. This process is automatic and transparent to the user.

```python
import tls_requests
r = tls_requests.get("https://httpbin.org/get", tls_identifier="chrome_120")
print(r)  # Output: <Response [200 OK]>

```

* * *

Supported Client Profiles
-------------------------

### Internal Profiles

#### Chrome

*   103 (`chrome_103`)
*   104 (`chrome_104`)
*   105 (`chrome_105`)
*   106 (`chrome_106`)
*   107 (`chrome_107`)
*   108 (`chrome_108`)
*   109 (`chrome_109`)
*   110 (`chrome_110`)
*   111 (`chrome_111`)
*   112 (`chrome_112`)
*   116 with PSK (`chrome_116_PSK`)
*   116 with PSK and PQ (`chrome_116_PSK_PQ`)
*   117 (`chrome_117`)
*   120 (`chrome_120`)
*   124 (`chrome_124`)
*   131 (`chrome_131`)
*   131 with PSK (`chrome_131_PSK`)

#### Safari

*   15.6.1 (`safari_15_6_1`)
*   16.0 (`safari_16_0`)

#### iOS (Safari)

*   15.5 (`safari_ios_15_5`)
*   15.6 (`safari_ios_15_6`)
*   16.0 (`safari_ios_16_0`)
*   17.0 (`safari_ios_17_0`)

#### iPadOS (Safari)

*   15.6 (`safari_ios_15_6`)

#### Firefox

*   102 (`firefox_102`)
*   104 (`firefox_104`)
*   105 (`firefox_105`)
*   106 (`firefox_106`)
*   108 (`firefox_108`)
*   110 (`firefox_110`)
*   117 (`firefox_117`)
*   120 (`firefox_120`)
*   123 (`firefox_123`)
*   132 (`firefox_132`)

#### Opera

*   89 (`opera_89`)
*   90 (`opera_90`)
*   91 (`opera_91`)

* * *

### Custom Profiles

*   Zalando iOS Mobile (`zalando_ios_mobile`)
*   Nike iOS Mobile (`nike_ios_mobile`)
*   Cloudscraper
*   MMS iOS (`mms_ios` or `mms_ios_1`)
*   MMS iOS 2 (`mms_ios_2`)
*   MMS iOS 3 (`mms_ios_3`)
*   Mesh iOS (`mesh_ios` or `mesh_ios_1`)
*   Mesh Android (`mesh_android` or `mesh_android_1`)
*   Mesh Android 2 (`mesh_android_2`)
*   Confirmed iOS (`confirmed_ios`)
*   Zalando Android Mobile (`zalando_android_mobile`)
*   Confirmed Android (`confirmed_android`)
*   Confirmed Android 2 (`confirmed_android_2`)

#### OkHttp4

*   Android 7 (`okhttp4_android_7`)
*   Android 8 (`okhttp4_android_8`)
*   Android 9 (`okhttp4_android_9`)
*   Android 10 (`okhttp4_android_10`)
*   Android 11 (`okhttp4_android_11`)
*   Android 12 (`okhttp4_android_12`)
*   Android 13 (`okhttp4_android_13`)
