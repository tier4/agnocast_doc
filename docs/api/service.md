
# Service

<!-- Auto-generated — do not edit. Regenerate with: doxygen Doxyfile && python3 generate_api_reference.py -->


### `agnocast::Service<ServiceT>`

Agnocast service server. The callback signature is void(const ipc_shared_ptr<RequestT>&, ipc_shared_ptr<ResponseT>&). The service/client API is experimental and may change in future versions.

**Example:**

```cpp
using SrvT = example_interfaces::srv::AddTwoInts;
using RequestT = agnocast::Service<SrvT>::RequestT;
using ResponseT = agnocast::Service<SrvT>::ResponseT;

auto service = agnocast::create_service<SrvT>(
  this, "add_two_ints",
  [this](const agnocast::ipc_shared_ptr<RequestT> & req,
         agnocast::ipc_shared_ptr<ResponseT> & res) {
    res->sum = req->a + req->b;
  });
```


---

#### `RequestT`

```cpp
struct RequestT
```

Request type extending ServiceT::Request with internal metadata. Received in the service callback's first argument.

| Template Parameter | Description |
|-----------|-------------|
| `RequestT` | Request message type (derived from `ServiceT::Request`). |


---

#### `ResponseT`

```cpp
struct ResponseT
```

Response type extending ServiceT::Response with internal metadata. Populated in the service callback's second argument.

| Template Parameter | Description |
|-----------|-------------|
| `ResponseT` | Response message type (derived from `ServiceT::Response`). |

