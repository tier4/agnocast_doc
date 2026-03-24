
# TakeSubscription

<!-- Auto-generated — do not edit. Regenerate with: doxygen Doxyfile && python3 generate_api_reference.py -->


### `agnocast::TakeSubscription<MessageT>`

**Extends:** `agnocast::SubscriptionBase`

Polling-based subscription that retrieves messages on demand via take(). Unlike BasicSubscription, no callback is invoked automatically. Call take() to retrieve the latest message. Useful in timer callbacks or control loops.


---

#### `take()`

```cpp
agnocast::ipc_shared_ptr<MessageT> TakeSubscription::take(bool allow_same_message)
```

Retrieve the latest message from the topic.

| Template Parameter | Description |
|-----------|-------------|
| `MessageT` | ROS message type. |
| **Parameter** | **Default** | **Description** |
| `allow_same_message` | `false` | If true, may return the same message as the previous call (useful for always having the latest value). If false, returns only new messages since the last take. |
| | | |
| **Returns** | Shared pointer to the message, or empty if unavailable. |

