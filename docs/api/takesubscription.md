
# TakeSubscription

<!-- Auto-generated — do not edit. Regenerate with: doxygen Doxyfile && python3 generate_api_reference.py -->


### `agnocast::TakeSubscription<MessageT>`

Polling-based subscription that retrieves messages on demand via take().


---

#### `take()`

```cpp
agnocast::ipc_shared_ptr<const MessageT> TakeSubscription::take(bool allow_same_message)
```

Retrieve one message from the topic.

| Template Parameter | Description |
|-----------|-------------|
| `MessageT` | ROS message type. |

| Parameter | Default | Description |
|-----------|---------|-------------|
| `allow_same_message` | `false` | If true, returns the oldest entry within the subscription's history depth, and may return the same message as the previous call. If false, returns the oldest entry not yet received by this subscriber, i.e. FIFO. |

| | |
|-----------|-------------|
| **Returns** | Shared pointer to the message, or empty if unavailable. |

