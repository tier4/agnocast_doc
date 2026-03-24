
# Executors

<!-- Auto-generated — do not edit. Regenerate with: doxygen Doxyfile && python3 generate_api_reference.py -->


### `agnocast::AgnocastExecutor`

**Extends:** `rclcpp::Executor`

Base class for Stage 1 executors that handle both ROS 2 (RMW) and Agnocast callbacks. Inherits from `rclcpp::Executor`.


---

#### `AgnocastExecutor() (constructor)`

```cpp
AgnocastExecutor::AgnocastExecutor(rclcpp::ExecutorOptions &options)
```

Construct the executor.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `options` | `rclcpp::ExecutorOptions()` | Executor options. |


---

#### `spin()`

```cpp
void AgnocastExecutor::spin()
```

Block the calling thread and process callbacks in a loop until `rclcpp::shutdown`() is called or the executor is cancelled.


### `agnocast::SingleThreadedAgnocastExecutor`

**Extends:** `agnocast::AgnocastExecutor`

Single-threaded executor for Stage 1 that processes both ROS 2 and Agnocast callbacks on one thread.


---

#### `SingleThreadedAgnocastExecutor() (constructor)`

```cpp
SingleThreadedAgnocastExecutor::SingleThreadedAgnocastExecutor(rclcpp::ExecutorOptions &options, int next_exec_timeout_ms)
```

Construct the executor.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `options` | `rclcpp::ExecutorOptions()` | Executor options. |
| `next_exec_timeout_ms` | `50` | Timeout in ms for waiting on the next executable. |


---

#### `spin()`

```cpp
void SingleThreadedAgnocastExecutor::spin()
```

Block the calling thread and process callbacks in a loop until `rclcpp::shutdown`() is called or the executor is cancelled.


### `agnocast::MultiThreadedAgnocastExecutor`

**Extends:** `agnocast::AgnocastExecutor`

Multi-threaded executor for Stage 1 with configurable thread counts for ROS 2 and Agnocast callbacks.


---

#### `MultiThreadedAgnocastExecutor() (constructor)`

```cpp
MultiThreadedAgnocastExecutor::MultiThreadedAgnocastExecutor(rclcpp::ExecutorOptions &options, size_t number_of_ros2_threads, size_t number_of_agnocast_threads, bool yield_before_execute, std::chrono::nanoseconds ros2_next_exec_timeout, int agnocast_next_exec_timeout_ms)
```

Construct the executor.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `options` | `rclcpp::ExecutorOptions()` | Executor options. |
| `number_of_ros2_threads` | `0` | Number of threads for ROS 2 callbacks (0 = auto). |
| `number_of_agnocast_threads` | `0` | Number of threads for Agnocast callbacks (0 = auto). |
| `yield_before_execute` | `false` | If true, call `std::this_thread::yield`() before each callback execution to reduce CPU usage at the cost of latency. |
| `ros2_next_exec_timeout` | `std::chrono::nanoseconds(-1)` | Timeout for ROS 2 executables. |
| `agnocast_next_exec_timeout_ms` | `50` | Timeout in ms for Agnocast executables. |


---

#### `spin()`

```cpp
void MultiThreadedAgnocastExecutor::spin()
```

Block the calling thread and process callbacks in a loop until `rclcpp::shutdown`() is called or the executor is cancelled.


### `agnocast::CallbackIsolatedAgnocastExecutor`

**Extends:** `rclcpp::Executor`

Callback-isolated executor for Stage 1. Assigns a dedicated thread to each callback group, ensuring that callbacks in different groups never run concurrently on the same thread. Handles both ROS 2 and Agnocast callbacks.


---

#### `CallbackIsolatedAgnocastExecutor() (constructor)`

```cpp
CallbackIsolatedAgnocastExecutor::CallbackIsolatedAgnocastExecutor(rclcpp::ExecutorOptions &options, int next_exec_timeout_ms, int monitor_polling_interval_ms)
```

Construct the executor.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `options` | `rclcpp::ExecutorOptions()` | Executor options. |
| `next_exec_timeout_ms` | `50` | Timeout in ms for waiting on the next executable. |
| `monitor_polling_interval_ms` | `100` | Polling interval in ms for monitoring new callback groups. |


---

#### `spin()`

```cpp
void CallbackIsolatedAgnocastExecutor::spin()
```

Block the calling thread and process callbacks in a loop until `rclcpp::shutdown`() is called or the executor is cancelled.


---

#### `cancel()`

```cpp
void CallbackIsolatedAgnocastExecutor::cancel()
```

Request the executor to stop spinning. Causes the current or next spin() call to return.


---

#### `add_callback_group()`

```cpp
void CallbackIsolatedAgnocastExecutor::add_callback_group(rclcpp::CallbackGroup::SharedPtr group_ptr, rclcpp::node_interfaces::NodeBaseInterface::SharedPtr node_ptr, bool notify)
```

Add a callback group to this executor.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `group_ptr` | — | Callback group to add. |
| `node_ptr` | — | Node the group belongs to. |
| `notify` | `true` | If true, wake the executor so it picks up the change immediately. |


---

#### `get_all_callback_groups()`

```cpp
std::vector<rclcpp::CallbackGroup::WeakPtr> CallbackIsolatedAgnocastExecutor::get_all_callback_groups()
```

Return all callback groups known to this executor.

| | |
|-----------|-------------|
| **Returns** | Vector of weak pointers to callback groups. |


---

#### `get_manually_added_callback_groups()`

```cpp
std::vector<rclcpp::CallbackGroup::WeakPtr> CallbackIsolatedAgnocastExecutor::get_manually_added_callback_groups()
```

Return callback groups that were manually added.

| | |
|-----------|-------------|
| **Returns** | Vector of weak pointers to callback groups. |


---

#### `get_automatically_added_callback_groups_from_nodes()`

```cpp
std::vector<rclcpp::CallbackGroup::WeakPtr> CallbackIsolatedAgnocastExecutor::get_automatically_added_callback_groups_from_nodes()
```

Return callback groups automatically discovered from added nodes.

| | |
|-----------|-------------|
| **Returns** | Vector of weak pointers to callback groups. |


---

#### `remove_callback_group()`

```cpp
void CallbackIsolatedAgnocastExecutor::remove_callback_group(rclcpp::CallbackGroup::SharedPtr group_ptr, bool notify)
```

Remove a callback group from this executor.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `group_ptr` | — | Callback group to remove. |
| `notify` | `true` | If true, wake the executor so it picks up the change immediately. |


---

#### `add_node()`

```cpp
void CallbackIsolatedAgnocastExecutor::add_node(rclcpp::node_interfaces::NodeBaseInterface::SharedPtr node_ptr, bool notify)
```

Add a node to this executor.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `node_ptr` | — | Node to add. |
| `notify` | `true` | If true, wake the executor so it picks up the change immediately. |


---

#### `add_node() [overload 2]`

```cpp
void CallbackIsolatedAgnocastExecutor::add_node(rclcpp::Node::SharedPtr node_ptr, bool notify)
```

Add a node to this executor.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `node_ptr` | — | Node to add. |
| `notify` | `true` | If true, wake the executor so it picks up the change immediately. |


---

#### `remove_node()`

```cpp
void CallbackIsolatedAgnocastExecutor::remove_node(rclcpp::node_interfaces::NodeBaseInterface::SharedPtr node_ptr, bool notify)
```

Remove a node from this executor.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `node_ptr` | — | Node to remove. |
| `notify` | `true` | If true, wake the executor so it picks up the change immediately. |


---

#### `remove_node() [overload 2]`

```cpp
void CallbackIsolatedAgnocastExecutor::remove_node(rclcpp::Node::SharedPtr node_ptr, bool notify)
```

Remove a node from this executor.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `node_ptr` | — | Node to remove. |
| `notify` | `true` | If true, wake the executor so it picks up the change immediately. |


### `agnocast::AgnocastOnlyExecutor`

Base class for Stage 2 executors that handle only Agnocast callbacks (no RMW). Used with `agnocast::Node`.


---

#### `AgnocastOnlyExecutor() (constructor)`

```cpp
AgnocastOnlyExecutor::AgnocastOnlyExecutor()
```

Construct the executor.


---

#### `spin()`

```cpp
void AgnocastOnlyExecutor::spin()
```

Block the calling thread and process Agnocast callbacks in a loop until cancel() is called.


---

#### `cancel()`

```cpp
void AgnocastOnlyExecutor::cancel()
```

Request the executor to stop spinning. Causes the current or next spin() call to return.


---

#### `add_callback_group()`

```cpp
void AgnocastOnlyExecutor::add_callback_group(rclcpp::CallbackGroup::SharedPtr group_ptr, rclcpp::node_interfaces::NodeBaseInterface::SharedPtr node_ptr, bool notify)
```

Add a callback group to this executor.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `group_ptr` | — | Callback group to add. |
| `node_ptr` | — | Node the group belongs to. |
| `notify` | `true` | If true, wake the executor so it picks up the change immediately. |


---

#### `remove_callback_group()`

```cpp
void AgnocastOnlyExecutor::remove_callback_group(rclcpp::CallbackGroup::SharedPtr group_ptr, bool notify)
```

Remove a callback group from this executor.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `group_ptr` | — | Callback group to remove. |
| `notify` | `true` | If true, wake the executor so it picks up the change immediately. |


---

#### `get_all_callback_groups()`

```cpp
std::vector<rclcpp::CallbackGroup::WeakPtr> AgnocastOnlyExecutor::get_all_callback_groups()
```

Return all callback groups known to this executor.

| | |
|-----------|-------------|
| **Returns** | Vector of weak pointers to callback groups. |


---

#### `get_manually_added_callback_groups()`

```cpp
std::vector<rclcpp::CallbackGroup::WeakPtr> AgnocastOnlyExecutor::get_manually_added_callback_groups()
```

Return callback groups that were manually added.

| | |
|-----------|-------------|
| **Returns** | Vector of weak pointers to callback groups. |


---

#### `get_automatically_added_callback_groups_from_nodes()`

```cpp
std::vector<rclcpp::CallbackGroup::WeakPtr> AgnocastOnlyExecutor::get_automatically_added_callback_groups_from_nodes()
```

Return callback groups automatically discovered from added nodes.

| | |
|-----------|-------------|
| **Returns** | Vector of weak pointers to callback groups. |


---

#### `add_node()`

```cpp
void AgnocastOnlyExecutor::add_node(rclcpp::node_interfaces::NodeBaseInterface::SharedPtr node_ptr, bool notify)
```

Add a node to this executor.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `node_ptr` | — | Node to add. |
| `notify` | `true` | If true, wake the executor so it picks up the change immediately. |


---

#### `add_node() [overload 2]`

```cpp
void AgnocastOnlyExecutor::add_node(std::shared_ptr<agnocast::Node> &node, bool notify)
```

Add a node to this executor.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `node` | — | Node to add. |
| `notify` | `true` | If true, wake the executor so it picks up the change immediately. |


---

#### `remove_node()`

```cpp
void AgnocastOnlyExecutor::remove_node(rclcpp::node_interfaces::NodeBaseInterface::SharedPtr node_ptr, bool notify)
```

Remove a node from this executor.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `node_ptr` | — | Node to remove. |
| `notify` | `true` | If true, wake the executor so it picks up the change immediately. |


---

#### `remove_node() [overload 2]`

```cpp
void AgnocastOnlyExecutor::remove_node(std::shared_ptr<agnocast::Node> &node, bool notify)
```

Remove a node from this executor.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `node` | — | Node to remove. |
| `notify` | `true` | If true, wake the executor so it picks up the change immediately. |


### `agnocast::AgnocastOnlySingleThreadedExecutor`

**Extends:** `agnocast::AgnocastOnlyExecutor`

Single-threaded executor for Stage 2 (Agnocast-only). Used with `agnocast::Node`.


---

#### `AgnocastOnlySingleThreadedExecutor() (constructor)`

```cpp
AgnocastOnlySingleThreadedExecutor::AgnocastOnlySingleThreadedExecutor(int next_exec_timeout_ms)
```

Construct the executor.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `next_exec_timeout_ms` | `50` | Timeout in ms for waiting on the next executable. |


---

#### `spin()`

```cpp
void AgnocastOnlySingleThreadedExecutor::spin()
```

Block the calling thread and process Agnocast callbacks in a loop until cancel() is called.


### `agnocast::AgnocastOnlyMultiThreadedExecutor`

**Extends:** `agnocast::AgnocastOnlyExecutor`

Multi-threaded executor for Stage 2 (Agnocast-only) with configurable thread count. Used with `agnocast::Node`.


---

#### `AgnocastOnlyMultiThreadedExecutor() (constructor)`

```cpp
AgnocastOnlyMultiThreadedExecutor::AgnocastOnlyMultiThreadedExecutor(size_t number_of_threads, bool yield_before_execute, int next_exec_timeout_ms)
```

Construct the executor.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `number_of_threads` | `0` | Number of threads (0 = auto). |
| `yield_before_execute` | `false` | Yield before executing each callback. |
| `next_exec_timeout_ms` | `50` | Timeout in ms for Agnocast executables. |


---

#### `spin()`

```cpp
void AgnocastOnlyMultiThreadedExecutor::spin()
```

Block the calling thread and process Agnocast callbacks in a loop until cancel() is called.


### `agnocast::AgnocastOnlyCallbackIsolatedExecutor`

**Extends:** `agnocast::AgnocastOnlyExecutor`

Callback-isolated executor for Stage 2 (Agnocast-only). Assigns a dedicated thread to each callback group. Used with `agnocast::Node`.


---

#### `AgnocastOnlyCallbackIsolatedExecutor() (constructor)`

```cpp
AgnocastOnlyCallbackIsolatedExecutor::AgnocastOnlyCallbackIsolatedExecutor(int next_exec_timeout_ms)
```

Construct the executor.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `next_exec_timeout_ms` | `50` | Timeout in ms for waiting on the next executable. |


---

#### `~AgnocastOnlyCallbackIsolatedExecutor() (destructor)`

```cpp
AgnocastOnlyCallbackIsolatedExecutor::~AgnocastOnlyCallbackIsolatedExecutor()
```

Destroy the executor and clean up child threads.


---

#### `spin()`

```cpp
void AgnocastOnlyCallbackIsolatedExecutor::spin()
```

Block the calling thread and process Agnocast callbacks in a loop until cancel() is called.


---

#### `cancel()`

```cpp
void AgnocastOnlyCallbackIsolatedExecutor::cancel()
```

Request the executor to stop spinning. Causes the current or next spin() call to return.


---

#### `add_node()`

```cpp
void AgnocastOnlyCallbackIsolatedExecutor::add_node(rclcpp::node_interfaces::NodeBaseInterface::SharedPtr &node_ptr, bool notify)
```

Add a node to this executor. Unlike the base class add_node() , this does NOT set the has_executor atomic flag on the node or its callback groups, because the CIE distributes callback groups to child executors which claim ownership individually.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `node_ptr` | — | Node to add. |
| `notify` | `false` | If true, wake the executor so it picks up the change immediately. |


---

#### `add_node() [overload 2]`

```cpp
void AgnocastOnlyCallbackIsolatedExecutor::add_node(agnocast::Node::SharedPtr &node_ptr, bool notify)
```

Add a node to this executor.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `node_ptr` | — | Node to add. |
| `notify` | `false` | If true, wake the executor so it picks up the change immediately. |

