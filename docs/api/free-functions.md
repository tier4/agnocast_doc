
# Free Functions (Stage 1)

<!-- Auto-generated — do not edit. Regenerate with: doxygen Doxyfile && python3 generate_api_reference.py -->

These free functions are used with `rclcpp::Node` at Stage 1. Pass the node pointer as the first argument.


---

#### `create_publisher()`

```cpp
agnocast::Publisher<MessageT>::SharedPtr create_publisher(NodeT *node, std::string &topic_name, rclcpp::QoS &qos, agnocast::PublisherOptions &options)
```

Create an Agnocast publisher (Stage 1 free function, QoS overload).

| Template Parameter | Description |
|-----------|-------------|
| `MessageT` | ROS message type. |
| `NodeT` | Node type (`rclcpp::Node` or `agnocast::Node`). |
| **Parameter** | **Default** | **Description** |
| `node` | — | Pointer to the node. |
| `topic_name` | — | Topic name. |
| `qos` | — | Quality of service profile. |
| `options` | `agnocast::PublisherOptions{}` | Publisher options. |
| | | |
| **Returns** | Shared pointer to the created publisher. |


---

#### `create_publisher() [overload 2]`

```cpp
agnocast::Publisher<MessageT>::SharedPtr create_publisher(NodeT *node, std::string &topic_name, size_t qos_history_depth, agnocast::PublisherOptions &options)
```

Create an Agnocast publisher (Stage 1 free function, history-depth overload).

| Template Parameter | Description |
|-----------|-------------|
| `MessageT` | ROS message type. |
| `NodeT` | Node type (`rclcpp::Node` or `agnocast::Node`). |
| **Parameter** | **Default** | **Description** |
| `node` | — | Pointer to the node. |
| `topic_name` | — | Topic name. |
| `qos_history_depth` | — | History depth for the QoS profile. |
| `options` | `agnocast::PublisherOptions{}` | Publisher options. |
| | | |
| **Returns** | Shared pointer to the created publisher. |


---

#### `create_subscription()`

```cpp
agnocast::Subscription<MessageT>::SharedPtr create_subscription(NodeT *node, std::string &topic_name, rclcpp::QoS &qos, Func &&callback, agnocast::SubscriptionOptions options)
```

Create an Agnocast subscription (Stage 1 free function, QoS overload).

| Template Parameter | Description |
|-----------|-------------|
| `MessageT` | ROS message type. |
| `NodeT` | Node type (`rclcpp::Node` or `agnocast::Node`). |
| `Func` | Callback callable with void(`agnocast::ipc_shared_ptr`<const MessageT>&&). |
| **Parameter** | **Default** | **Description** |
| `node` | — | Pointer to the node. |
| `topic_name` | — | Topic name. |
| `qos` | — | Quality of service profile. |
| `callback` | — | Callback invoked on each received message. |
| `options` | `agnocast::SubscriptionOptions{}` | Subscription options. |
| | | |
| **Returns** | Shared pointer to the created subscription. |


---

#### `create_subscription() [overload 2]`

```cpp
agnocast::Subscription<MessageT>::SharedPtr create_subscription(NodeT *node, std::string &topic_name, size_t qos_history_depth, Func &&callback, agnocast::SubscriptionOptions options)
```

Create an Agnocast subscription (Stage 1 free function, history-depth overload).

| Template Parameter | Description |
|-----------|-------------|
| `MessageT` | ROS message type. |
| `NodeT` | Node type (`rclcpp::Node` or `agnocast::Node`). |
| `Func` | Callback callable with void(`agnocast::ipc_shared_ptr`<const MessageT>&&). |
| **Parameter** | **Default** | **Description** |
| `node` | — | Pointer to the node. |
| `topic_name` | — | Topic name. |
| `qos_history_depth` | — | History depth for the QoS profile. |
| `callback` | — | Callback invoked on each received message. |
| `options` | `agnocast::SubscriptionOptions{}` | Subscription options. |
| | | |
| **Returns** | Shared pointer to the created subscription. |


---

#### `create_subscription() [overload 3]`

```cpp
agnocast::PollingSubscriber<MessageT>::SharedPtr create_subscription(NodeT *node, std::string &topic_name, size_t qos_history_depth)
```

Create an Agnocast polling subscription (Stage 1 free function, history-depth overload).

| Template Parameter | Description |
|-----------|-------------|
| `MessageT` | ROS message type. |
| `NodeT` | Node type (`rclcpp::Node` or `agnocast::Node`). |
| **Parameter** | **Description** |
| `node` | Pointer to the node. |
| `topic_name` | Topic name. |
| `qos_history_depth` | History depth for the QoS profile. |
| | |
| **Returns** | Shared pointer to the created polling subscription. |


---

#### `create_subscription() [overload 4]`

```cpp
agnocast::PollingSubscriber<MessageT>::SharedPtr create_subscription(NodeT *node, std::string &topic_name, rclcpp::QoS &qos)
```

Create an Agnocast polling subscription (Stage 1 free function, QoS overload).

| Template Parameter | Description |
|-----------|-------------|
| `MessageT` | ROS message type. |
| `NodeT` | Node type (`rclcpp::Node` or `agnocast::Node`). |
| **Parameter** | **Description** |
| `node` | Pointer to the node. |
| `topic_name` | Topic name. |
| `qos` | Quality of service profile. |
| | |
| **Returns** | Shared pointer to the created polling subscription. |


---

#### `create_client()`

```cpp
agnocast::Client<ServiceT>::SharedPtr create_client(rclcpp::Node *node, std::string &service_name, rclcpp::QoS &qos, rclcpp::CallbackGroup::SharedPtr group)
```

Create an Agnocast service client (Stage 1 free function).

| Template Parameter | Description |
|-----------|-------------|
| `ServiceT` | ROS service type. |
| **Parameter** | **Default** | **Description** |
| `node` | — | Pointer to `rclcpp::Node`. |
| `service_name` | — | Service name. |
| `qos` | `rclcpp::ServicesQoS()` | Quality of service profile. |
| `group` | `nullptr` | Callback group (nullptr = default). |
| | | |
| **Returns** | Shared pointer to the created client. |


---

#### `create_service()`

```cpp
agnocast::Service<ServiceT>::SharedPtr create_service(rclcpp::Node *node, std::string &service_name, Func &&callback, rclcpp::QoS &qos, rclcpp::CallbackGroup::SharedPtr group)
```

Create an Agnocast service server (Stage 1 free function).

| Template Parameter | Description |
|-----------|-------------|
| `ServiceT` | ROS service type. |
| `Func` | Callable with signature void(const `agnocast::ipc_shared_ptr`<const RequestT>&, / `agnocast::ipc_shared_ptr`<ResponseT>&). |
| **Parameter** | **Default** | **Description** |
| `node` | — | Pointer to `rclcpp::Node`. |
| `service_name` | — | Service name. |
| `callback` | — | Callback invoked on each request. |
| `qos` | `rclcpp::ServicesQoS()` | Quality of service profile. |
| `group` | `nullptr` | Callback group (nullptr = default). |
| | | |
| **Returns** | Shared pointer to the created service. |


---

#### `create_timer()`

```cpp
agnocast::TimerBase::SharedPtr create_timer(NodeT node, rclcpp::Clock::SharedPtr clock, rclcpp::Duration period, CallbackT &&callback, rclcpp::CallbackGroup::SharedPtr group, bool autostart)
```

Create a timer with a given clock. This free function mirrors the `rclcpp::create_timer`() API for portability.

| Template Parameter | Description |
|-----------|-------------|
| `NodeT` | Node type (`rclcpp::Node` or `agnocast::Node`). |
| `CallbackT` | Callable type for the callback. |
| **Parameter** | **Default** | **Description** |
| `node` | — | Node providing get_node_base_interface() for the default callback group. |
| `clock` | — | Clock to drive the timer. |
| `period` | — | Time interval between triggers of the callback. |
| `callback` | — | User-defined callback function. |
| `group` | `nullptr` | Callback group to execute this timer's callback in. |
| `autostart` | `true` | Whether to start the timer immediately (not yet supported; always true). |
| | | |
| **Returns** | Shared pointer to the created timer. |


---

#### `init()`

```cpp
void init(int argc, char **argv)
```

Initialize Agnocast. Must be called once before creating any `agnocast::Node` . This is the counterpart of `rclcpp::init`() for `agnocast::Node` .

| Parameter | Description |
|-----------|-------------|
| `argc` | Number of command-line arguments. |
| `argv` | Command-line argument array. |


---

#### `shutdown()`

```cpp
void shutdown()
```

Shut down Agnocast. Should be called before process exit in `agnocast::Node` processes. This is the counterpart of `rclcpp::shutdown`() for `agnocast::Node`.

