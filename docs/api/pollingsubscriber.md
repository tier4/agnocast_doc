
# PollingSubscriber

<!-- Auto-generated — do not edit. Regenerate with: doxygen Doxyfile && python3 generate_api_reference.py -->


### `agnocast::PollingSubscriber<MessageT>`

Polling subscription that retrieves messages on demand. Wraps TakeSubscription with a simplified interface.

**Example:**

```cpp
// Polling subscription — call take_data() in a timer callback
auto sub = this->create_subscription<MyMsg>("/topic", rclcpp::QoS(1));

auto timer = this->create_wall_timer(100ms, [this, sub]() {
  auto msg = sub->take_data();
  if (msg) {
    RCLCPP_INFO(get_logger(), "Polled: %d", msg->data);
  }
});
```


---

#### `take_data()`

```cpp
agnocast::ipc_shared_ptr<MessageT> PollingSubscriber::take_data()
```

Retrieve the latest message. Always returns the most recent message even if already retrieved. Returns an empty pointer if no message has been published yet.

| Template Parameter | Description |
|-----------|-------------|
| `MessageT` | ROS message type. |
| | |
| **Returns** | Shared pointer to the latest message. |

