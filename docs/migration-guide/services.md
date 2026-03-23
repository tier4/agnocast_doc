# Services

Agnocast supports ROS 2-style services with zero-copy request and response handling via shared memory.

!!! warning
    Agnocast service/client is not officially supported yet. The API may introduce breaking changes without a major version increment. Use at your own risk.

## Migrating a Service Server

### Before (rclcpp)

```cpp
#include "rclcpp/rclcpp.hpp"
#include "my_package/srv/my_service.hpp"

using ServiceT = my_package::srv::MyService;
using RequestT = ServiceT::Request;
using ResponseT = ServiceT::Response;

class MyServer : public rclcpp::Node
{
  rclcpp::Service<ServiceT>::SharedPtr service_;

public:
  MyServer() : Node("my_server")
  {
    service_ = create_service<ServiceT>(
      "my_service",
      [this](const std::shared_ptr<RequestT> request,
             std::shared_ptr<ResponseT> response) {
        response->result = process(request->data);
        RCLCPP_INFO(get_logger(), "Processed request");
      });
  }
};
```

### After (Agnocast Stage 1)

```cpp
#include "agnocast/agnocast.hpp"                                       // (1)
#include "my_package/srv/my_service.hpp"

using ServiceT = my_package::srv::MyService;
using RequestT = agnocast::Service<ServiceT>::RequestT;                // (2)
using ResponseT = agnocast::Service<ServiceT>::ResponseT;              // (2)

class MyServer : public rclcpp::Node
{
  agnocast::Service<ServiceT>::SharedPtr service_;                     // (3)

public:
  MyServer() : Node("my_server")
  {
    service_ = agnocast::create_service<ServiceT>(                     // (4)
      this, "my_service",
      [this](const agnocast::ipc_shared_ptr<RequestT> & request,      // (5)
             agnocast::ipc_shared_ptr<ResponseT> & response) {
        response->result = process(request->data);
        RCLCPP_INFO(get_logger(), "Processed request");
      });
  }
};
```

Key changes:

1. Include changes to `agnocast/agnocast.hpp`
2. Type aliases change to `agnocast::Service<ServiceT>::RequestT` / `ResponseT`
3. `rclcpp::Service` → `agnocast::Service`
4. Use free function `agnocast::create_service(this, ...)` instead of `this->create_service(...)`
5. Callback takes `agnocast::ipc_shared_ptr` references instead of `std::shared_ptr`

### After (Agnocast Stage 2)

```cpp
#include "agnocast/agnocast.hpp"
#include "my_package/srv/my_service.hpp"

using ServiceT = my_package::srv::MyService;
using RequestT = agnocast::Service<ServiceT>::RequestT;
using ResponseT = agnocast::Service<ServiceT>::ResponseT;

class MyServer : public agnocast::Node                                 // (1)
{
  agnocast::Service<ServiceT>::SharedPtr service_;

public:
  MyServer() : Node("my_server")
  {
    service_ = this->create_service<ServiceT>(                         // (2)
      "my_service",
      [this](const agnocast::ipc_shared_ptr<RequestT> & request,
             agnocast::ipc_shared_ptr<ResponseT> & response) {
        response->result = process(request->data);
        RCLCPP_INFO(get_logger(), "Processed request");
      });
  }
};
```

Additional changes from Stage 1:

1. Base class changes to `agnocast::Node`
2. Service creation uses member function instead of free function

## Migrating a Service Client

### Before (rclcpp)

```cpp
auto client = node->create_client<ServiceT>("my_service");

while (!client->wait_for_service(1s)) {
  RCLCPP_INFO(node->get_logger(), "Waiting for service...");
}

auto request = std::make_shared<ServiceT::Request>();
request->data = 42;
client->async_send_request(
  request,
  [](rclcpp::Client<ServiceT>::SharedFuture future) {
    auto response = future.get();
    // process response
  });
```

### After (Agnocast Stage 1)

```cpp
auto client = agnocast::create_client<ServiceT>(                       // (1)
  node.get(), "my_service");

while (!client->wait_for_service(1s)) {
  RCLCPP_INFO(node->get_logger(), "Waiting for service...");
}

auto request = client->borrow_loaned_request();                        // (2)
request->data = 42;
client->async_send_request(
  std::move(request),                                                  // (3)
  [](agnocast::Client<ServiceT>::SharedFuture future) {                // (4)
    auto response = future.get();
    // process response
  });
```

Key changes:

1. Use free function `agnocast::create_client(node.get(), ...)`
2. Allocate request via `borrow_loaned_request()` (shared memory) instead of `std::make_shared`
3. Pass request with `std::move` (zero-copy handoff)
4. Future type changes to `agnocast::Client<ServiceT>::SharedFuture`

### After (Agnocast Stage 2)

```cpp
auto client = node->create_client<ServiceT>("my_service");             // (1)
// Same usage pattern as Stage 1
```

Additional change from Stage 1:

1. Client creation uses member function instead of free function
