# Stage 2: agnocast::Node

In Stage 2, you replace `rclcpp::Node` with `agnocast::Node`. This bypasses the rcl layer entirely — no RMW participant is created — reducing launch time and CPU usage.

!!! warning "Prerequisite"
    Stage 2 can only be applied to a node once **all** publishers and subscriptions in that node have been migrated to Agnocast APIs (Stage 1 complete).

## Migrating a Publisher

### Before (Stage 1)

```cpp
#include "agnocast/agnocast.hpp"
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

class MyPublisher : public rclcpp::Node
{
  agnocast::Publisher<std_msgs::msg::String>::SharedPtr pub_;
  rclcpp::TimerBase::SharedPtr timer_;

  void timer_callback()
  {
    auto msg = pub_->borrow_loaned_message();
    msg->data = "Hello, world!";
    pub_->publish(std::move(msg));
  }

public:
  MyPublisher() : Node("my_publisher")
  {
    auto group = create_callback_group(rclcpp::CallbackGroupType::MutuallyExclusive);

    pub_ = agnocast::create_publisher<std_msgs::msg::String>(
      this, "/topic", 10);
    timer_ = create_wall_timer(100ms,
      std::bind(&MyPublisher::timer_callback, this), group);
  }
};
```

### After (Stage 2)

```cpp
#include "agnocast/agnocast.hpp"
#include "std_msgs/msg/string.hpp"

class MyPublisher : public agnocast::Node                           // (1)
{
  agnocast::Publisher<std_msgs::msg::String>::SharedPtr pub_;
  agnocast::TimerBase::SharedPtr timer_;                            // (2)

  void timer_callback()
  {
    auto msg = pub_->borrow_loaned_message();
    msg->data = "Hello, world!";
    pub_->publish(std::move(msg));
  }

public:
  MyPublisher() : Node("my_publisher")
  {
    auto group = create_callback_group(rclcpp::CallbackGroupType::MutuallyExclusive);

    pub_ = this->create_publisher<std_msgs::msg::String>(           // (3)
      "/topic", 10);
    timer_ = this->create_wall_timer(100ms,
      std::bind(&MyPublisher::timer_callback, this), group);
  }
};
```

Key changes:

1. Base class changes from `rclcpp::Node` to `agnocast::Node`
2. Timer type changes to `agnocast::TimerBase::SharedPtr`
3. Publisher creation uses member function `this->create_publisher(...)` instead of free function

## Migrating a Subscription

### Before (Stage 1)

```cpp
#include "agnocast/agnocast.hpp"
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

class MySubscriber : public rclcpp::Node
{
  agnocast::Subscription<std_msgs::msg::String>::SharedPtr sub_;

  void callback(const agnocast::ipc_shared_ptr<std_msgs::msg::String> & msg)
  {
    RCLCPP_INFO(get_logger(), "Received: %s", msg->data.c_str());
  }

public:
  MySubscriber() : Node("my_subscriber")
  {
    auto group = create_callback_group(rclcpp::CallbackGroupType::MutuallyExclusive);
    agnocast::SubscriptionOptions options;
    options.callback_group = group;

    sub_ = agnocast::create_subscription<std_msgs::msg::String>(
      this, "/topic", 10,
      std::bind(&MySubscriber::callback, this, std::placeholders::_1),
      options);
  }
};
```

### After (Stage 2)

```cpp
#include "agnocast/agnocast.hpp"
#include "std_msgs/msg/string.hpp"

class MySubscriber : public agnocast::Node                          // (1)
{
  agnocast::Subscription<std_msgs::msg::String>::SharedPtr sub_;

  void callback(const agnocast::ipc_shared_ptr<std_msgs::msg::String> & msg)
  {
    RCLCPP_INFO(get_logger(), "Received: %s", msg->data.c_str());
  }

public:
  MySubscriber() : Node("my_subscriber")
  {
    auto group = create_callback_group(rclcpp::CallbackGroupType::MutuallyExclusive);
    agnocast::SubscriptionOptions options;
    options.callback_group = group;

    sub_ = this->create_subscription<std_msgs::msg::String>(        // (2)
      "/topic", 10,
      std::bind(&MySubscriber::callback, this, std::placeholders::_1),
      options);
  }
};
```

Key changes:

1. Base class changes to `agnocast::Node`
2. Subscription creation uses member function instead of free function

## Switching the Executor (Nodes with `main`)

Replace the initialization and executor.

**Before (Stage 1):**

```cpp
int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  agnocast::SingleThreadedAgnocastExecutor executor;
  auto node = std::make_shared<MyNode>();
  executor.add_node(node);
  executor.spin();
  rclcpp::shutdown();
}
```

**After (Stage 2):**

```cpp
int main(int argc, char * argv[])
{
  agnocast::init(argc, argv);                                       // (1)
  agnocast::AgnocastOnlySingleThreadedExecutor executor;            // (2)
  auto node = std::make_shared<MyNode>();
  executor.add_node(node);
  executor.spin();
}
```

Key changes:

1. `rclcpp::init()` → `agnocast::init()`, `rclcpp::shutdown()` no longer needed
2. Executor changes to `AgnocastOnly*` variant

Available executors for Stage 2:

| Executor |
|----------|
| `agnocast::AgnocastOnlySingleThreadedExecutor` |
| `agnocast::AgnocastOnlyMultiThreadedExecutor` |
| `agnocast::AgnocastOnlyCallbackIsolatedExecutor` |

!!! note
    If a process contains a mix of `rclcpp::Node` (Stage 1) and `agnocast::Node` (Stage 2) nodes, use the non-`AgnocastOnly` executors (e.g., `agnocast::CallbackIsolatedAgnocastExecutor`), which can handle both.

## Switching the Executor (Composable Nodes)

Replace the `EXECUTOR` option with an `AgnocastOnly*` variant.

**CMakeLists.txt (before — Stage 1):**

```cmake
agnocast_components_register_node(
  my_component
  PLUGIN "MyNode"
  EXECUTABLE my_node
)
```

**CMakeLists.txt (after — Stage 2):**

```cmake
agnocast_components_register_node(
  my_component
  PLUGIN "MyNode"
  EXECUTABLE my_node
  EXECUTOR AgnocastOnlySingleThreadedExecutor
)
```

No launch file changes are needed from Stage 1 — `LD_PRELOAD` and the container executable remain the same.

## Supplementary Information

### agnocast::Node API Compatibility

`agnocast::Node` provides an API largely compatible with `rclcpp::Node`, but some APIs are not yet supported. Before migrating to Stage 2, check the [agnocast::Node interface comparison](https://github.com/autowarefoundation/agnocast/blob/main/docs/agnocast_node_interface_comparison.md) to confirm the APIs your node uses are supported.

### Summary of Changes from Stage 1 to Stage 2

| Aspect | Stage 1 | Stage 2 |
|--------|---------|---------|
| Node class | `rclcpp::Node` | `agnocast::Node` |
| Pub/sub creation | `agnocast::create_*(this, ...)` | `this->create_*(...)` |
| Initialization | `rclcpp::init()` | `agnocast::init()` |
| Executor | `agnocast::*AgnocastExecutor` | `agnocast::AgnocastOnly*Executor` |
| rclcpp dependency | Required | Not required |
| RMW participant | Created | Not created |
