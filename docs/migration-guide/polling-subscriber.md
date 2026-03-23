# Polling Subscriber

Agnocast provides `agnocast::PollingSubscriber`, a pull-based subscription that lets you fetch the latest message on demand rather than receiving it via a callback. This corresponds to the `subscription->take()` pattern in rclcpp, but returns a zero-copy shared pointer from shared memory instead of copying data into a provided message.

`PollingSubscriber` is available at both Stage 1 (`rclcpp::Node`) and Stage 2 (`agnocast::Node`).

## Migration from rclcpp `take()`

### Before (rclcpp)

```cpp
class MyPollingNode : public rclcpp::Node
{
  rclcpp::Subscription<std_msgs::msg::String>::SharedPtr sub_;
  rclcpp::TimerBase::SharedPtr timer_;

  void timer_callback()
  {
    std_msgs::msg::String msg;
    rclcpp::MessageInfo msg_info;
    if (sub_->take(msg, msg_info)) {
      RCLCPP_INFO(get_logger(), "Polled: %s", msg.data.c_str());
    }
  }

public:
  MyPollingNode() : Node("my_polling_node")
  {
    sub_ = create_subscription<std_msgs::msg::String>(
      "/topic", rclcpp::QoS(rclcpp::KeepLast(1)),
      [](std_msgs::msg::String::SharedPtr) {});  // dummy callback required by rclcpp

    timer_ = create_wall_timer(1s,
      std::bind(&MyPollingNode::timer_callback, this));
  }
};
```

### After (Agnocast Stage 1)

```cpp
class MyPollingNode : public rclcpp::Node
{
  agnocast::PollingSubscriber<std_msgs::msg::String>::SharedPtr sub_;  // (1)
  rclcpp::TimerBase::SharedPtr timer_;

  void timer_callback()
  {
    auto msg = sub_->take_data();                                      // (2)
    if (msg) {
      RCLCPP_INFO(get_logger(), "Polled: %s", msg->data.c_str());
    }
  }

public:
  MyPollingNode() : Node("my_polling_node")
  {
    sub_ = agnocast::create_subscription<std_msgs::msg::String>(       // (3)
      this, "/topic", rclcpp::QoS(rclcpp::KeepLast(1)));

    timer_ = create_wall_timer(1s,
      std::bind(&MyPollingNode::timer_callback, this));
  }
};
```

Key changes:

1. `rclcpp::Subscription` → `agnocast::PollingSubscriber` (no dummy callback needed)
2. `sub_->take(msg, msg_info)` → `sub_->take_data()` which returns an `agnocast::ipc_shared_ptr<const T>` (zero-copy)
3. Use `agnocast::create_subscription` free function (no callback argument)

### After (Agnocast Stage 2)

```cpp
class MyPollingNode : public agnocast::Node                            // (1)
{
  agnocast::PollingSubscriber<std_msgs::msg::String>::SharedPtr sub_;
  agnocast::TimerBase::SharedPtr timer_;                               // (2)

  void timer_callback()
  {
    auto msg = sub_->take_data();
    if (msg) {
      RCLCPP_INFO(get_logger(), "Polled: %s", msg->data.c_str());
    }
  }

public:
  MyPollingNode() : Node("my_polling_node")
  {
    sub_ = this->create_subscription<std_msgs::msg::String>(           // (3)
      "/topic", rclcpp::QoS(rclcpp::KeepLast(1)));

    timer_ = this->create_wall_timer(1s,
      std::bind(&MyPollingNode::timer_callback, this));
  }
};
```

Additional changes from Stage 1:

1. Base class changes to `agnocast::Node`
2. Timer type changes to `agnocast::TimerBase::SharedPtr`
3. Subscription creation uses member function instead of free function
