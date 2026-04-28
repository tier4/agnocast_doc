
# Publisher

<!-- Auto-generated — do not edit. Regenerate with: doxygen Doxyfile && python3 generate_api_reference.py -->


### `agnocast::Publisher<MessageT>`

Zero-copy publisher that allocates messages in shared memory. Use borrow_loaned_message() to obtain a message, populate its fields, then call publish() to transfer it to subscribers without copying.

**Example:**

```cpp
// Create a publisher (Stage 1, with rclcpp::Node)
auto pub = agnocast::create_publisher<MyMsg>(this, "/topic", 10);

// Borrow, populate, publish
auto msg = pub->borrow_loaned_message();
msg->data = 42;
pub->publish(std::move(msg));  // msg is invalidated after this
```


---

#### `borrow_loaned_message()`

```cpp
agnocast::ipc_shared_ptr<MessageT> Publisher::borrow_loaned_message()
```

Allocate a new default-constructed message in shared memory. The caller must either pass the returned pointer to publish() or let it go out of scope (which frees the memory).

| Template Parameter | Description |
|-----------|-------------|
| `MessageT` | ROS message type. |
| | |
| **Returns** | Owned pointer to the newly allocated message in shared memory. |


---

#### `publish()`

```cpp
void Publisher::publish(agnocast::ipc_shared_ptr<MessageT> &&message)
```

Publish a message via zero-copy IPC. Ownership is transferred: after this call, the passed-in ipc_shared_ptr and all copies sharing its control block are invalidated — dereferencing them calls `std::terminate`().

| Template Parameter | Description |
|-----------|-------------|
| `MessageT` | ROS message type. |
| **Parameter** | **Description** |
| `message` | Message obtained from borrow_loaned_message(). Must be moved in. |


---

#### `get_subscription_count()`

```cpp
uint32_t Publisher::get_subscription_count() const
```

Return the total subscriber count for this topic (Agnocast + ROS 2 via bridge).

| | |
|-----------|-------------|
| **Returns** | Total subscriber count. |


---

#### `get_gid()`

```cpp
rmw_gid_t & Publisher::get_gid() const
```

Return the GID of this publisher, unique across both Agnocast and ROS 2.

| | |
|-----------|-------------|
| **Returns** | Publisher GID. |


---

#### `get_intra_subscription_count()`

```cpp
uint32_t Publisher::get_intra_subscription_count() const
```

Return the number of Agnocast intra-process subscribers only (excludes ROS 2).

| | |
|-----------|-------------|
| **Returns** | Agnocast subscriber count. |


---

#### `get_topic_name()`

```cpp
char * Publisher::get_topic_name() const
```

Return the fully-resolved topic name.

| | |
|-----------|-------------|
| **Returns** | Null-terminated topic name string. |

