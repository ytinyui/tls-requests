Hooks
===========================

TLS Requests supports hooks, enabling you to execute custom logic during specific events in the HTTP request/response lifecycle.
These hooks are perfect for logging, monitoring, tracing, or pre/post-processing requests and responses.


* * *

Hook Types
----------

### 1\. **Request Hook**

Executed after the request is fully prepared but before being sent to the network. It receives the `request` object, enabling inspection or modification.

### 2\. **Response Hook**

Triggered after the response is fetched from the network but before being returned to the caller. It receives the `response` object, allowing inspection or processing.


* * *

Setting Up Hooks
----------------

Hooks are registered by providing a dictionary with keys `'request'` and/or `'response'`, and their values are lists of callable functions.

### Example 1: Logging Requests and Responses

```python
def log_request(request):
    print(f"Request event hook: {request.method} {request.url} - Waiting for response")

def log_response(response):
    request = response.request
    print(f"Response event hook: {request.method} {request.url} - Status {response.status_code}")

client = tls_requests.Client(hooks={'request': [log_request], 'response': [log_response]})
```

* * *

### Example 2: Raising Errors on 4xx and 5xx Responses

```python
def raise_on_4xx_5xx(response):
    response.raise_for_status()

client = tls_requests.Client(hooks={'response': [raise_on_4xx_5xx]})
```

### Example 3: Adding a Timestamp Header to Requests

```python
import datetime

def add_timestamp(request):
    request.headers['x-request-timestamp'] = datetime.datetime.utcnow().isoformat()

client = tls_requests.Client(hooks={'request': [add_timestamp]})
response = client.get('https://httpbin.org/get')
print(response.text)
```

* * *

Managing Hooks
--------------

### Setting Hooks During Client Initialization

Provide a dictionary of hooks when creating the client:

```python
client = tls_requests.Client(hooks={
    'request': [log_request],
    'response': [log_response, raise_on_4xx_5xx],
})
```

### Dynamically Updating Hooks

Use the `.hooks` property to inspect or modify hooks after the client is created:

```python
client = tls_requests.Client()

# Add hooks
client.hooks['request'] = [log_request]
client.hooks['response'] = [log_response]

# Replace hooks
client.hooks = {
    'request': [log_request],
    'response': [log_response, raise_on_4xx_5xx],
}
```

Best Practices
--------------

1.  **Access Content**: Use `.read()` or `await .aread()` in asynchronous contexts to access `response.content` before returning it.
2.  **Always Use Lists:** Hooks must be registered as **lists of callables**, even if you are adding only one function.
3.  **Combine Hooks:** You can register multiple hooks for the same event type to handle various concerns, such as logging and error handling.
4.  **Order Matters:** Hooks are executed in the order they are registered.

With hooks, TLS Requests provides a flexible mechanism to seamlessly integrate monitoring, logging, or custom behaviors into your HTTP workflows.
