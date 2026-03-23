# Stage 1: Agnocast Pub/Sub

In Stage 1, you keep `rclcpp::Node` as the node base class and rewrite only the publishers, subscriptions, and smart pointers to use Agnocast APIs. This gives you true zero-copy IPC with minimal code changes. Agnocast and rclcpp publishers/subscriptions can coexist within the same node, so you can migrate topic by topic.

## Build Setup

Add `agnocastlib` to your CMake dependencies.

**CMakeLists.txt:**

```cmake
find_package(agnocastlib REQUIRED)

ament_target_dependencies(your_target agnocastlib)
```

!!! warning "Do not add agnocastlib to package.xml"
    Do **not** declare `<depend>agnocastlib</depend>` in your `package.xml`. Because Agnocast uses version-pinned installation, adding it to `package.xml` would cause `rosdep install` to automatically pull in a different version, breaking the version alignment between components. Agnocast dependencies are managed through the [environment setup](../environment-setup/index.md) instead.

## Migrating a Publisher

### Before (rclcpp)

```cpp
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

class MyPublisher : public rclcpp::Node
{
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr pub_;
  rclcpp::TimerBase::SharedPtr timer_;

  void timer_callback()
  {
    auto msg = std_msgs::msg::String();
    msg.data = "Hello, world!";
    pub_->publish(msg);
  }

public:
  MyPublisher() : Node("my_publisher")
  {
    auto group = create_callback_group(rclcpp::CallbackGroupType::MutuallyExclusive);

    pub_ = create_publisher<std_msgs::msg::String>("/topic", 10);
    timer_ = create_wall_timer(100ms,
      std::bind(&MyPublisher::timer_callback, this), group);
  }
};
```

### After (Agnocast Stage 1)

```cpp
#include "agnocast/agnocast.hpp"                                    // (1)
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

class MyPublisher : public rclcpp::Node                             // Node unchanged
{
  agnocast::Publisher<std_msgs::msg::String>::SharedPtr pub_;        // (2)
  rclcpp::TimerBase::SharedPtr timer_;

  void timer_callback()
  {
    auto msg = pub_->borrow_loaned_message();                       // (3)
    msg->data = "Hello, world!";
    pub_->publish(std::move(msg));                                  // (4)
  }

public:
  MyPublisher() : Node("my_publisher")
  {
    auto group = create_callback_group(rclcpp::CallbackGroupType::MutuallyExclusive);

    pub_ = agnocast::create_publisher<std_msgs::msg::String>(       // (5)
      this, "/topic", 10);
    timer_ = create_wall_timer(100ms,
      std::bind(&MyPublisher::timer_callback, this), group);
  }
};
```

Key changes:

1. Add `#include "agnocast/agnocast.hpp"`
2. Change `rclcpp::Publisher` → `agnocast::Publisher`
3. Allocate messages via `borrow_loaned_message()` (writes to shared memory)
4. Publish with `std::move(msg)` (zero-copy handoff)
5. Use free function `agnocast::create_publisher(this, ...)` instead of `this->create_publisher(...)`

## Migrating a Subscription

### Before (rclcpp)

```cpp
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

class MySubscriber : public rclcpp::Node
{
  rclcpp::Subscription<std_msgs::msg::String>::SharedPtr sub_;

  void callback(const std_msgs::msg::String::SharedPtr msg)
  {
    RCLCPP_INFO(get_logger(), "Received: %s", msg->data.c_str());
  }

public:
  MySubscriber() : Node("my_subscriber")
  {
    auto group = create_callback_group(rclcpp::CallbackGroupType::MutuallyExclusive);
    rclcpp::SubscriptionOptions options;
    options.callback_group = group;

    sub_ = create_subscription<std_msgs::msg::String>(
      "/topic", 10,
      std::bind(&MySubscriber::callback, this, std::placeholders::_1),
      options);
  }
};
```

### After (Agnocast Stage 1)

```cpp
#include "agnocast/agnocast.hpp"                                    // (1)
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

class MySubscriber : public rclcpp::Node                            // Node unchanged
{
  agnocast::Subscription<std_msgs::msg::String>::SharedPtr sub_;    // (2)

  void callback(
    const agnocast::ipc_shared_ptr<std_msgs::msg::String> & msg)    // (3)
  {
    RCLCPP_INFO(get_logger(), "Received: %s", msg->data.c_str());
  }

public:
  MySubscriber() : Node("my_subscriber")
  {
    auto group = create_callback_group(rclcpp::CallbackGroupType::MutuallyExclusive);
    agnocast::SubscriptionOptions options;                          // (4)
    options.callback_group = group;

    sub_ = agnocast::create_subscription<std_msgs::msg::String>(    // (5)
      this, "/topic", 10,
      std::bind(&MySubscriber::callback, this, std::placeholders::_1),
      options);
  }
};
```

Key changes:

1. Add `#include "agnocast/agnocast.hpp"`
2. Change `rclcpp::Subscription` → `agnocast::Subscription`
3. Callback takes `const agnocast::ipc_shared_ptr<T> &` instead of `T::SharedPtr`
4. Change `rclcpp::SubscriptionOptions` → `agnocast::SubscriptionOptions`
5. Use free function `agnocast::create_subscription(this, ...)` instead of `this->create_subscription(...)`

## Switching the Executor (Nodes with `main`)

Replace the executor with an Agnocast executor.

**Before:**

```cpp
int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);

  rclcpp::executors::SingleThreadedExecutor executor;
  auto node = std::make_shared<MyNode>();
  executor.add_node(node);
  executor.spin();

  rclcpp::shutdown();
}
```

**After:**

```cpp
int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);                                         // unchanged

  agnocast::SingleThreadedAgnocastExecutor executor;
  auto node = std::make_shared<MyNode>();
  executor.add_node(node);
  executor.spin();

  rclcpp::shutdown();
}
```

Available executors for Stage 1:

| Executor |
|----------|
| `agnocast::SingleThreadedAgnocastExecutor` |
| `agnocast::MultiThreadedAgnocastExecutor` |
| `agnocast::CallbackIsolatedAgnocastExecutor` (Agnocast-compatible version of [callback_isolated_executor](https://github.com/autowarefoundation/callback_isolated_executor)) |

## Switching the Executor (Composable Nodes)

No changes to node source code are needed beyond the pub/sub migration. Replace `rclcpp_components_register_node` with `agnocast_components_register_node` in CMakeLists.txt.

**CMakeLists.txt (before):**

```cmake
find_package(rclcpp_components REQUIRED)

rclcpp_components_register_node(
  my_component
  PLUGIN "MyNode"
  EXECUTABLE my_node
)
```

**CMakeLists.txt (after):**

```cmake
find_package(agnocast_components REQUIRED)

agnocast_components_register_node(
  my_component
  PLUGIN "MyNode"
  EXECUTABLE my_node
)
```

The `EXECUTOR` option controls which executor the standalone executable uses (defaults to `SingleThreadedAgnocastExecutor`):

```cmake
agnocast_components_register_node(
  my_component
  PLUGIN "MyNode"
  EXECUTABLE my_node
  EXECUTOR CallbackIsolatedAgnocastExecutor
)
```

When loading into a component container instead, the container executable determines the executor:

| Container executable | Executor |
|---------------------|----------|
| `agnocast_component_container` | `SingleThreadedAgnocastExecutor` |
| `agnocast_component_container_mt` | `MultiThreadedAgnocastExecutor` |
| `agnocast_component_container_cie` | `CallbackIsolatedAgnocastExecutor` |

## Launch File

Add `LD_PRELOAD` for `libagnocast_heaphook.so` so that ROS message memory is allocated in shared memory. For composable nodes, also switch to the Agnocast component container.

!!! warning
    `libagnocast_heaphook.so` cannot be used together with other libraries that hook the same memory allocation functions.

**Standalone node (before):**

```xml
<node pkg="my_package" exec="my_node" name="my_node" output="screen">
</node>
```

**Standalone node (after):**

```xml
<node pkg="my_package" exec="my_node" name="my_node" output="screen">
    <env name="LD_PRELOAD" value="libagnocast_heaphook.so:$(env LD_PRELOAD '')" />
</node>
```

**Component container (before):**

```xml
<node_container pkg="rclcpp_components" exec="component_container"
                name="my_container" namespace="" output="screen">
    <composable_node pkg="my_package" plugin="MyNode"
                     name="my_node" namespace="">
    </composable_node>
</node_container>
```

**Component container (after):**

```xml
<node_container pkg="agnocast_components" exec="agnocast_component_container"
                name="my_container" namespace="" output="screen">
    <env name="LD_PRELOAD" value="libagnocast_heaphook.so:$(env LD_PRELOAD '')" />

    <composable_node pkg="my_package" plugin="MyNode"
                     name="my_node" namespace="">
    </composable_node>
</node_container>
```

## Next Step

Once all publishers and subscriptions in a node have been migrated to Agnocast, you can proceed to [Stage 2](stage2.md) to gain additional performance by switching to `agnocast::Node`.
