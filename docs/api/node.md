
# Node

<!-- Auto-generated — do not edit. Regenerate with: doxygen Doxyfile && python3 generate_api_reference.py -->


### `agnocast::Node`

Agnocast-only node. Drop-in replacement for `rclcpp::Node` in pure-Agnocast processes.


---

#### `Node() (constructor)`

```cpp
Node::Node(std::string &node_name, rclcpp::NodeOptions &options)
```

Construct a node with the given name.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `node_name` | — | Name of the node. |
| `options` | `rclcpp::NodeOptions()` | Node options. |


---

#### `Node() (constructor) [overload 2]`

```cpp
Node::Node(std::string &node_name, std::string &namespace_, rclcpp::NodeOptions &options)
```

Construct a node with the given name and namespace.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `node_name` | — | Name of the node. |
| `namespace_` | — | Namespace of the node. |
| `options` | `rclcpp::NodeOptions()` | Node options. |


---

#### `get_name()`

```cpp
std::string Node::get_name() const
```

Return the name of the node.

| | |
|-----------|-------------|
| **Returns** | Node name. |


---

#### `get_logger()`

```cpp
rclcpp::Logger Node::get_logger() const
```

Return the logger associated with this node.

| | |
|-----------|-------------|
| **Returns** | Logger instance. |


---

#### `get_namespace()`

```cpp
std::string Node::get_namespace() const
```

Return the namespace of the node.

| | |
|-----------|-------------|
| **Returns** | Node namespace. |


---

#### `get_fully_qualified_name()`

```cpp
std::string Node::get_fully_qualified_name() const
```

Return the fully qualified name (namespace + node name).

| | |
|-----------|-------------|
| **Returns** | Fully qualified name string. |


---

#### `create_callback_group()`

```cpp
rclcpp::CallbackGroup::SharedPtr Node::create_callback_group(rclcpp::CallbackGroupType group_type, bool automatically_add_to_executor_with_node)
```

Create a callback group.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `group_type` | — | Type of callback group. |
| `automatically_add_to_executor_with_node` | `true` | Whether to auto-add to executor. |
| | | |
| **Returns** | Shared pointer to the created callback group. |


---

#### `for_each_callback_group()`

```cpp
void Node::for_each_callback_group(rclcpp::node_interfaces::NodeBaseInterface::CallbackGroupFunction &func)
```

Iterate over all callback groups, invoking the given function on each.


---

#### `declare_parameter()`

```cpp
rclcpp::ParameterValue& Node::declare_parameter(std::string &name, rclcpp::ParameterValue &default_value, rcl_interfaces::msg::ParameterDescriptor &descriptor, bool ignore_override)
```

Declare a parameter with a default value.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `name` | — | Parameter name. |
| `default_value` | — | Default value. |
| `descriptor` | `rcl_interfaces::msg::ParameterDescriptor{}` | Optional descriptor. |
| `ignore_override` | `false` | If true, ignore launch-file overrides. |
| | | |
| **Returns** | The parameter value. |


---

#### `declare_parameter() [overload 2]`

```cpp
rclcpp::ParameterValue& Node::declare_parameter(std::string &name, rclcpp::ParameterType type, rcl_interfaces::msg::ParameterDescriptor &descriptor, bool ignore_override)
```

Declare a parameter with a given type (no default value).

| Parameter | Default | Description |
|-----------|---------|-------------|
| `name` | — | Parameter name. |
| `type` | — | Parameter type. |
| `descriptor` | `rcl_interfaces::msg::ParameterDescriptor{}` | Optional descriptor. |
| `ignore_override` | `false` | If true, ignore launch-file overrides. |
| | | |
| **Returns** | The parameter value. |


---

#### `declare_parameter() [overload 3]`

```cpp
auto Node::declare_parameter(std::string &name, ParameterT &default_value, rcl_interfaces::msg::ParameterDescriptor &descriptor, bool ignore_override)
```

Declare a parameter with a typed default value.

| Template Parameter | Description |
|-----------|-------------|
| `ParameterT` | C++ type of the parameter. |
| **Parameter** | **Default** | **Description** |
| `name` | — | Parameter name. |
| `default_value` | — | Default value. |
| `descriptor` | `rcl_interfaces::msg::ParameterDescriptor{}` | Optional descriptor. |
| `ignore_override` | `false` | If true, ignore launch-file overrides. |
| | | |
| **Returns** | The parameter value. |


---

#### `declare_parameter() [overload 4]`

```cpp
auto Node::declare_parameter(std::string &name, rcl_interfaces::msg::ParameterDescriptor &descriptor, bool ignore_override)
```

Declare a parameter using only its type (default-constructed).

| Template Parameter | Description |
|-----------|-------------|
| `ParameterT` | C++ type of the parameter. |
| **Parameter** | **Default** | **Description** |
| `name` | — | Parameter name. |
| `descriptor` | `rcl_interfaces::msg::ParameterDescriptor{}` | Optional descriptor. |
| `ignore_override` | `false` | If true, ignore launch-file overrides. |
| | | |
| **Returns** | The parameter value. |


---

#### `has_parameter()`

```cpp
bool Node::has_parameter(std::string &name) const
```

Check whether a parameter has been declared.

| | |
|-----------|-------------|
| **Returns** | True if the parameter exists. |


---

#### `undeclare_parameter()`

```cpp
void Node::undeclare_parameter(std::string &name)
```

Undeclare a previously declared parameter.


---

#### `get_parameter()`

```cpp
rclcpp::Parameter Node::get_parameter(std::string &name) const
```

Get a parameter by name.

| | |
|-----------|-------------|
| **Returns** | The requested parameter. |


---

#### `get_parameter() [overload 2]`

```cpp
bool Node::get_parameter(std::string &name, rclcpp::Parameter &parameter) const
```

Get a parameter by name, returning success status via bool.

| | |
|-----------|-------------|
| **Returns** | True if the parameter was found. |


---

#### `get_parameter() [overload 3]`

```cpp
bool Node::get_parameter(std::string &name, ParameterT &parameter) const
```

Get a parameter and extract its typed value.

| Template Parameter | Description |
|-----------|-------------|
| `ParameterT` | C++ type to extract. |
| | |
| **Returns** | True if the parameter was found. |


---

#### `get_parameters()`

```cpp
std::vector<rclcpp::Parameter> Node::get_parameters(std::vector<std::string> &names) const
```

Get multiple parameters by name.

| | |
|-----------|-------------|
| **Returns** | Vector of requested parameters. |


---

#### `get_parameters() [overload 2]`

```cpp
bool Node::get_parameters(std::string &prefix, std::map<std::string, ParameterT> &values) const
```

Get parameters matching a prefix into a typed map.

| Template Parameter | Description |
|-----------|-------------|
| `ParameterT` | C++ type to extract. |
| | |
| **Returns** | True if any parameters matched the prefix. |


---

#### `set_parameter()`

```cpp
rcl_interfaces::msg::SetParametersResult Node::set_parameter(rclcpp::Parameter &parameter)
```

Set a single parameter.

| | |
|-----------|-------------|
| **Returns** | Result of the set operation. |


---

#### `set_parameters()`

```cpp
std::vector<rcl_interfaces::msg::SetParametersResult> Node::set_parameters(std::vector<rclcpp::Parameter> &parameters)
```

Set multiple parameters, one at a time.

| | |
|-----------|-------------|
| **Returns** | Vector of results. |


---

#### `set_parameters_atomically()`

```cpp
rcl_interfaces::msg::SetParametersResult Node::set_parameters_atomically(std::vector<rclcpp::Parameter> &parameters)
```

Set multiple parameters atomically (all-or-nothing).

| | |
|-----------|-------------|
| **Returns** | Result of the atomic operation. |


---

#### `describe_parameter()`

```cpp
rcl_interfaces::msg::rcl_interfaces::msg::ParameterDescriptor Node::describe_parameter(std::string &name) const
```

Describe a single parameter.

| | |
|-----------|-------------|
| **Returns** | Parameter descriptor. |


---

#### `describe_parameters()`

```cpp
std::vector<rcl_interfaces::msg::rcl_interfaces::msg::ParameterDescriptor> Node::describe_parameters(std::vector<std::string> &names) const
```

Describe multiple parameters.

| | |
|-----------|-------------|
| **Returns** | Vector of parameter descriptors. |


---

#### `get_parameter_types()`

```cpp
std::vector<uint8_t> Node::get_parameter_types(std::vector<std::string> &names) const
```

Get the types of the given parameters.

| | |
|-----------|-------------|
| **Returns** | Vector of parameter type identifiers. |


---

#### `list_parameters()`

```cpp
rcl_interfaces::msg::ListParametersResult Node::list_parameters(std::vector<std::string> &prefixes, uint64_t depth) const
```

List parameters matching the given prefixes up to the given depth.

| | |
|-----------|-------------|
| **Returns** | Matching parameter names and prefixes. |


---

#### `add_on_set_parameters_callback()`

```cpp
rclcpp::node_interfaces::OnSetParametersCallbackHandle::SharedPtr Node::add_on_set_parameters_callback(rclcpp::node_interfaces::OnSetParametersCallbackType callback)
```

Register a callback invoked before parameters are set.

| | |
|-----------|-------------|
| **Returns** | Handle to the registered callback. |


---

#### `remove_on_set_parameters_callback()`

```cpp
void Node::remove_on_set_parameters_callback(rclcpp::node_interfaces::OnSetParametersCallbackHandle *handler)
```

Remove a previously registered on-set-parameters callback.


---

#### `get_clock()`

```cpp
rclcpp::Clock::SharedPtr Node::get_clock()
```

Get the clock used by this node.

| | |
|-----------|-------------|
| **Returns** | Shared pointer to the clock. |


---

#### `get_clock() [overload 2]`

```cpp
rclcpp::Clock::ConstSharedPtr Node::get_clock() const
```

Get the clock used by this node (const).

| | |
|-----------|-------------|
| **Returns** | Shared pointer to the clock. |


---

#### `now()`

```cpp
rclcpp::Time Node::now() const
```

Return the current time according to this node's clock.

| | |
|-----------|-------------|
| **Returns** | Current time. |


---

#### `count_publishers()`

```cpp
size_t Node::count_publishers(std::string &topic_name) const
```

Return the number of publishers on a topic.

| | |
|-----------|-------------|
| **Returns** | Publisher count. |


---

#### `count_subscribers()`

```cpp
size_t Node::count_subscribers(std::string &topic_name) const
```

Return the number of subscribers on a topic.

| | |
|-----------|-------------|
| **Returns** | Subscriber count. |


---

#### `create_publisher()`

```cpp
agnocast::Publisher::SharedPtr Node::create_publisher(std::string &topic_name, rclcpp::QoS &qos, agnocast::PublisherOptions options)
```

Create a publisher (QoS overload).

| Template Parameter | Description |
|-----------|-------------|
| `MessageT` | ROS message type. |
| **Parameter** | **Default** | **Description** |
| `topic_name` | — | Topic name. |
| `qos` | — | Quality of service profile. |
| `options` | `agnocast::PublisherOptions{}` | Publisher options. |
| | | |
| **Returns** | Shared pointer to the created publisher. |


---

#### `create_publisher() [overload 2]`

```cpp
agnocast::Publisher::SharedPtr Node::create_publisher(std::string &topic_name, size_t queue_size, agnocast::PublisherOptions options)
```

Create a publisher (queue-size overload).

| Template Parameter | Description |
|-----------|-------------|
| `MessageT` | ROS message type. |
| **Parameter** | **Default** | **Description** |
| `topic_name` | — | Topic name. |
| `queue_size` | — | History depth for the QoS profile. |
| `options` | `agnocast::PublisherOptions{}` | Publisher options. |
| | | |
| **Returns** | Shared pointer to the created publisher. |


---

#### `create_subscription()`

```cpp
agnocast::Subscription::SharedPtr Node::create_subscription(std::string &topic_name, rclcpp::QoS &qos, Func &&callback, agnocast::SubscriptionOptions options)
```

Create a subscription (QoS overload).

| Template Parameter | Description |
|-----------|-------------|
| `MessageT` | ROS message type. |
| `Func` | Callback type. |
| **Parameter** | **Default** | **Description** |
| `topic_name` | — | Topic name. |
| `qos` | — | Quality of service profile. |
| `callback` | — | Callback invoked on each received message. |
| `options` | `agnocast::SubscriptionOptions{}` | Subscription options. |
| | | |
| **Returns** | Shared pointer to the created subscription. |


---

#### `create_subscription() [overload 2]`

```cpp
agnocast::Subscription::SharedPtr Node::create_subscription(std::string &topic_name, size_t queue_size, Func &&callback, agnocast::SubscriptionOptions options)
```

Create a subscription (queue-size overload).

| Template Parameter | Description |
|-----------|-------------|
| `MessageT` | ROS message type. |
| `Func` | Callback type. |
| **Parameter** | **Default** | **Description** |
| `topic_name` | — | Topic name. |
| `queue_size` | — | History depth for the QoS profile. |
| `callback` | — | Callback invoked on each received message. |
| `options` | `agnocast::SubscriptionOptions{}` | Subscription options. |
| | | |
| **Returns** | Shared pointer to the created subscription. |


---

#### `create_subscription() [overload 3]`

```cpp
agnocast::PollingSubscriber::SharedPtr Node::create_subscription(std::string &topic_name, size_t qos_history_depth)
```

Create a polling subscription (history-depth overload).

| Template Parameter | Description |
|-----------|-------------|
| `MessageT` | ROS message type. |
| **Parameter** | **Description** |
| `topic_name` | Topic name. |
| `qos_history_depth` | History depth for the QoS profile. |
| | |
| **Returns** | Shared pointer to the created polling subscription. |


---

#### `create_subscription() [overload 4]`

```cpp
agnocast::PollingSubscriber::SharedPtr Node::create_subscription(std::string &topic_name, rclcpp::QoS &qos)
```

Create a polling subscription (QoS overload).

| Template Parameter | Description |
|-----------|-------------|
| `MessageT` | ROS message type. |
| **Parameter** | **Description** |
| `topic_name` | Topic name. |
| `qos` | Quality of service profile. |
| | |
| **Returns** | Shared pointer to the created polling subscription. |


---

#### `create_wall_timer()`

```cpp
agnocast::WallTimer<CallbackT>::SharedPtr Node::create_wall_timer(std::chrono::duration<DurationRepT, DurationT> period, CallbackT callback, rclcpp::CallbackGroup::SharedPtr group, bool autostart)
```

Create a wall timer.

| Template Parameter | Description |
|-----------|-------------|
| `CallbackT` | Callable type for the callback. |
| **Parameter** | **Default** | **Description** |
| `period` | — | Timer period. |
| `callback` | — | Callback invoked on each tick. |
| `group` | `nullptr` | Callback group (nullptr = default). |
| `autostart` | `true` | Whether to start immediately (not yet supported; always true). |
| | | |
| **Returns** | Shared pointer to the created timer. |


---

#### `create_timer()`

```cpp
agnocast::GenericTimer<CallbackT>::SharedPtr Node::create_timer(std::chrono::duration<DurationRepT, DurationT> period, CallbackT callback, rclcpp::CallbackGroup::SharedPtr group, bool autostart)
```

Create a timer using the node's clock.

| Template Parameter | Description |
|-----------|-------------|
| `CallbackT` | Callable type for the callback. |
| **Parameter** | **Default** | **Description** |
| `period` | — | Timer period. |
| `callback` | — | Callback invoked on each tick. |
| `group` | `nullptr` | Callback group (nullptr = default). |
| `autostart` | `true` | Whether to start immediately (not yet supported; always true). |
| | | |
| **Returns** | Shared pointer to the created timer. |


---

#### `create_client()`

```cpp
agnocast::Client::SharedPtr Node::create_client(std::string &service_name, rclcpp::QoS &qos, rclcpp::CallbackGroup::SharedPtr group)
```

Create a service client.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `service_name` | — | Service name. |
| `qos` | `rclcpp::ServicesQoS()` | Quality of service profile. |
| `group` | `nullptr` | Callback group (nullptr = default). |
| | | |
| **Returns** | Shared pointer to the created client. |


---

#### `create_service()`

```cpp
agnocast::Service::SharedPtr Node::create_service(std::string &service_name, Func &&callback, rclcpp::QoS &qos, rclcpp::CallbackGroup::SharedPtr group)
```

Create a service server.

| Template Parameter | Description |
|-----------|-------------|
| `Func` | Callable with signature void(const `agnocast::ipc_shared_ptr`<const RequestT>&, `agnocast::ipc_shared_ptr`<ResponseT>&). |
| **Parameter** | **Default** | **Description** |
| `service_name` | — | Service name. |
| `callback` | — | Callback invoked on each request. |
| `qos` | `rclcpp::ServicesQoS()` | Quality of service profile. |
| `group` | `nullptr` | Callback group (nullptr = default). |
| | | |
| **Returns** | Shared pointer to the created service. |

