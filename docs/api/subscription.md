
# Subscription

<!-- Auto-generated — do not edit. Regenerate with: doxygen Doxyfile && python3 generate_api_reference.py -->


### `agnocast::Subscription<MessageT>`

**Extends:** `agnocast::SubscriptionBase`

Event-driven subscription that invokes a callback on each new message. The callback signature is `void(const `agnocast::ipc_shared_ptr`<const MessageT>&)`.

**Example:**

```cpp
// Event-driven subscription (Stage 1, with rclcpp::Node)
auto sub = agnocast::create_subscription<MyMsg>(
  this, "/topic", 10,
  [this](const agnocast::ipc_shared_ptr<const MyMsg> & msg) {
    RCLCPP_INFO(get_logger(), "Received: %d", msg->data);
  });
```

