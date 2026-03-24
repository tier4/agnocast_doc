
# Client

<!-- Auto-generated — do not edit. Regenerate with: doxygen Doxyfile && python3 generate_api_reference.py -->


### `agnocast::Client<ServiceT>`

Service client for zero-copy Agnocast service communication. The service/client API is experimental and may change in future versions.

**Example:**

```cpp
using SrvT = example_interfaces::srv::AddTwoInts;

auto client = agnocast::create_client<SrvT>(this, "add_two_ints");
client->wait_for_service();

// Send a request with a callback
auto req = client->borrow_loaned_request();
req->a = 1;
req->b = 2;
client->async_send_request(std::move(req),
  [this](agnocast::Client<SrvT>::SharedFuture future) {
    RCLCPP_INFO(get_logger(), "Result: %ld", future.get()->sum);
  });

// Or send a request and get a future
auto req2 = client->borrow_loaned_request();
req2->a = 3;
req2->b = 4;
auto future = client->async_send_request(std::move(req2));
RCLCPP_INFO(get_logger(), "Result: %ld", future.get()->sum);
```


---

#### `FutureAndRequestId`

```cpp
struct FutureAndRequestId
```

Return type of async_send_request() (no-callback overload). Contains a Future and the request ID. Access the future via the future member and the request ID via request_id.


---

#### `RequestT`

```cpp
struct RequestT
```

Request type extending ServiceT::Request with internal metadata. Use this in borrow_loaned_request() return types.

| Template Parameter | Description |
|-----------|-------------|
| `RequestT` | Request message type (derived from `ServiceT::Request`). |


---

#### `ResponseT`

```cpp
struct ResponseT
```

Response type extending ServiceT::Response with internal metadata. Received via Future or SharedFuture.

| Template Parameter | Description |
|-----------|-------------|
| `ResponseT` | Response message type (derived from `ServiceT::Response`). |


---

#### `SharedFutureAndRequestId`

```cpp
struct SharedFutureAndRequestId
```

Return type of async_send_request() (callback overload). Contains a SharedFuture and the request ID. Access the shared future via the future member and the request ID via request_id.


---

#### `Future`

```cpp
Future
```

Future that resolves to the service response. Returned by async_send_request() (no-callback overload).


---

#### `SharedFuture`

```cpp
SharedFuture
```

Shared future that resolves to the service response. Passed to the callback in async_send_request().


---

#### `borrow_loaned_request()`

```cpp
agnocast::ipc_shared_ptr<RequestT> Client::borrow_loaned_request()
```

Allocate a request message in shared memory.

| Template Parameter | Description |
|-----------|-------------|
| `RequestT` | Request message type (derived from `ServiceT::Request`). |
| | |
| **Returns** | Owned pointer to the request message in shared memory. |


---

#### `get_service_name()`

```cpp
char* Client::get_service_name() const
```

Return the resolved service name.

| | |
|-----------|-------------|
| **Returns** | Null-terminated service name string. |


---

#### `service_is_ready()`

```cpp
bool Client::service_is_ready() const
```

Check if the service server is available.

| | |
|-----------|-------------|
| **Returns** | True if the service server is available. |


---

#### `wait_for_service()`

```cpp
bool Client::wait_for_service(std::chrono::duration<RepT, RatioT> timeout) const
```

Block until the service is available or the timeout expires.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `timeout` | `std::chrono::nanoseconds(-1)` | Maximum duration to wait (-1 = wait forever). |
| | | |
| **Returns** | True if service became available, false on timeout. |


---

#### `async_send_request()`

```cpp
SharedFutureAndRequestId Client::async_send_request(agnocast::ipc_shared_ptr<RequestT> &&request, std::function<void(SharedFuture)> callback)
```

Send a request asynchronously and invoke a callback when the response arrives.

| Template Parameter | Description |
|-----------|-------------|
| `RequestT` | Request message type (derived from `ServiceT::Request`). |
| **Parameter** | **Description** |
| `request` | Request from borrow_loaned_request(). Must be moved in. |
| `callback` | Invoked with a SharedFuture when the response arrives. Call future.get() to obtain the response. |
| | |
| **Returns** | A SharedFutureAndRequestId containing the shared future (.future) and a sequence number (.request_id). |


---

#### `async_send_request() [overload 2]`

```cpp
FutureAndRequestId Client::async_send_request(agnocast::ipc_shared_ptr<RequestT> &&request)
```

Send a request asynchronously and return a future for the response.

| Template Parameter | Description |
|-----------|-------------|
| `RequestT` | Request message type (derived from `ServiceT::Request`). |
| **Parameter** | **Description** |
| `request` | Request from borrow_loaned_request(). Must be moved in. |
| | |
| **Returns** | A FutureAndRequestId containing the future (.future) and a sequence number (.request_id). Call .future.get() to block until the response arrives. |

