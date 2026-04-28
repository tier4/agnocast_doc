
# Message Filters

<!-- Auto-generated — do not edit. Regenerate with: doxygen Doxyfile && python3 generate_api_reference.py -->

Agnocast provides message synchronization filters compatible with the ROS 2 `message_filters` API. These allow you to synchronize messages from multiple Agnocast topics based on their timestamps.


### `agnocast::message_filters::MessageEvent<M>`

Wrapper around a message pointer that carries metadata for message filter pipelines.


---

#### `MessageEvent()`

```cpp
message_filters::MessageEvent<M>::MessageEvent()
```

Default-construct an empty MessageEvent.


---

#### `MessageEvent() [overload 2]`

```cpp
message_filters::MessageEvent<M>::MessageEvent(MessageEvent &rhs)
```

Copy constructor.


---

#### `MessageEvent() [overload 3]`

```cpp
message_filters::MessageEvent<M>::MessageEvent(ConstMessagePtr &message)
```

Construct from a message pointer, recording the current time as receipt time.


---

#### `MessageEvent() [overload 4]`

```cpp
message_filters::MessageEvent<M>::MessageEvent(ConstMessagePtr &message, rclcpp::Time receipt_time)
```

Construct from a message pointer and an explicit receipt time.


---

#### `operator=()`

```cpp
MessageEvent & message_filters::MessageEvent<M>::operator=(MessageEvent &rhs)
```

Copy assignment operator.


---

#### `getMessage()`

```cpp
ConstMessagePtr & message_filters::MessageEvent<M>::getMessage() const
```

Retrieve the message. Returns ipc_shared_ptr<M const> pointing to shared memory.


---

#### `getConstMessage()`

```cpp
ConstMessagePtr & message_filters::MessageEvent<M>::getConstMessage() const
```

Retrieve a const version of the message (same as getMessage() in agnocast)


---

#### `getReceiptTime()`

```cpp
rclcpp::Time message_filters::MessageEvent<M>::getReceiptTime() const
```

Returns the time at which this message was received.


---

#### `operator<()`

```cpp
bool message_filters::MessageEvent<M>::operator<(MessageEvent &rhs) const
```

Less-than comparison, ordered by pointer then receipt time.


### `agnocast::message_filters::SimpleFilter<M>`

**Extends:** `noncopyable`

Base class for simple one-output filters. Provides callback registration and signal dispatch.


---

#### `registerCallback()`

```cpp
Connection message_filters::SimpleFilter<M>::registerCallback(C &callback)
```

Register a callback to be invoked when a message passes through this filter.

| Parameter | Description |
|-----------|-------------|
| `callback` | Callback to register. |
| | |
| **Returns** | Connection object for disconnecting. |


---

#### `setName()`

```cpp
void message_filters::SimpleFilter<M>::setName(std::string &name)
```

Set the name of this filter (for debugging).

| Parameter | Description |
|-----------|-------------|
| `name` | Filter name. |


---

#### `getName()`

```cpp
std::string & message_filters::SimpleFilter<M>::getName() const
```

Return the name of this filter.

| | |
|-----------|-------------|
| **Returns** | Filter name string. |


### `agnocast::message_filters::SubscriberBase<M>`

Base class for Subscriber, allowing subscription management without knowing the message type. Used for type-erased subscriber collections.


---

#### `subscribe()`

```cpp
void message_filters::SubscriberBase<NodeType>::subscribe(NodePtr node, std::string &topic, rmw_qos_profile_t qos)
```

Subscribe to a topic. If this Subscriber is already subscribed to a topic, this function will first unsubscribe.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `node` | — | The `rclcpp::Node::SharedPtr` to use to subscribe. |
| `topic` | — | The topic to subscribe to. |
| `qos` | `rmw_qos_profile_default` | (optional) The rmw qos profile to use to subscribe. |


---

#### `subscribe() [overload 2]`

```cpp
void message_filters::SubscriberBase<NodeType>::subscribe(NodeType *node, std::string &topic, rmw_qos_profile_t qos)
```

Subscribe to a topic. If this Subscriber is already subscribed to a topic, this function will first unsubscribe.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `node` | — | The `rclcpp::Node` to use to subscribe. |
| `topic` | — | The topic to subscribe to. |
| `qos` | `rmw_qos_profile_default` | (optional) The rmw qos profile to use to subscribe. |


---

#### `subscribe() [overload 3]`

```cpp
void message_filters::SubscriberBase<NodeType>::subscribe(NodePtr node, std::string &topic, rmw_qos_profile_t qos, agnocast::SubscriptionOptions options)
```

Subscribe to a topic. If this Subscriber is already subscribed to a topic, this function will first unsubscribe. This override allows SubscriptionOptions to be passed into the class without changing API.

| Parameter | Description |
|-----------|-------------|
| `node` | The `rclcpp::Node::SharedPtr` to use to subscribe. |
| `topic` | The topic to subscribe to. |
| `qos` | The rmw qos profile to use to subscribe. |
| `options` | The subscription options to use to subscribe. |


---

#### `subscribe() [overload 4]`

```cpp
void message_filters::SubscriberBase<NodeType>::subscribe(NodeType *node, std::string &topic, rmw_qos_profile_t qos, agnocast::SubscriptionOptions options)
```

Subscribe to a topic. If this Subscriber is already subscribed to a topic, this function will first unsubscribe.

| Parameter | Description |
|-----------|-------------|
| `node` | The `rclcpp::Node` to use to subscribe. |
| `topic` | The topic to subscribe to. |
| `qos` | The rmw qos profile to use to subscribe. |
| `options` | The subscription options to use to subscribe. |


---

#### `subscribe() [overload 5]`

```cpp
void message_filters::SubscriberBase<NodeType>::subscribe()
```

Re-subscribe to a topic. Only works if this subscriber has previously been subscribed to a topic.


---

#### `unsubscribe()`

```cpp
void message_filters::SubscriberBase<NodeType>::unsubscribe()
```

Force immediate unsubscription of this subscriber from its topic.


### `agnocast::message_filters::Subscriber<M>`

**Extends:** `agnocast::message_filters::SubscriberBase< rclcpp::Node >`, `agnocast::message_filters::SimpleFilter< M >`

Agnocast subscription filter. This class acts as a highest-level filter, simply passing messages from an agnocast subscription through to the filters which have connected to it. When this object is destroyed it will unsubscribe from the agnocast subscription. The Subscriber object is templated on the type of message being subscribed to.


---

#### `Subscriber()`

```cpp
message_filters::Subscriber<M, NodeType>::Subscriber(NodePtr node, std::string &topic, rmw_qos_profile_t qos)
```

Constructor. See the `agnocast::create_subscription`() variants for more information on the parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `node` | — | The `rclcpp::Node::SharedPtr` to use to subscribe. |
| `topic` | — | The topic to subscribe to. |
| `qos` | `rmw_qos_profile_default` | (optional) The rmw qos profile to use to subscribe. |


---

#### `Subscriber() [overload 2]`

```cpp
message_filters::Subscriber<M, NodeType>::Subscriber(NodePtr node, std::string &topic, rmw_qos_profile_t qos, agnocast::SubscriptionOptions options)
```

Constructor. See the `agnocast::create_subscription`() variants for more information on the parameters

| Parameter | Description |
|-----------|-------------|
| `node` | The `rclcpp::Node::SharedPtr` to use to subscribe. |
| `topic` | The topic to subscribe to. |
| `qos` | The rmw qos profile to use to subscribe. |
| `options` | The subscription options to use to subscribe. |


---

#### `Subscriber() [overload 3]`

```cpp
message_filters::Subscriber<M, NodeType>::Subscriber()
```

Empty constructor, use subscribe() to subscribe to a topic.


---

#### `subscribe()`

```cpp
void message_filters::Subscriber<M, NodeType>::subscribe(NodePtr node, std::string &topic, rmw_qos_profile_t qos)
```

Subscribe to a topic. If this Subscriber is already subscribed to a topic, this function will first unsubscribe.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `node` | — | The `rclcpp::Node::SharedPtr` to use to subscribe. |
| `topic` | — | The topic to subscribe to. |
| `qos` | `rmw_qos_profile_default` | (optional) The rmw qos profile to use to subscribe. |


---

#### `subscribe() [overload 2]`

```cpp
void message_filters::Subscriber<M, NodeType>::subscribe(NodeType *node, std::string &topic, rmw_qos_profile_t qos)
```

Subscribe to a topic. If this Subscriber is already subscribed to a topic, this function will first unsubscribe.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `node` | — | The `rclcpp::Node` to use to subscribe. |
| `topic` | — | The topic to subscribe to. |
| `qos` | `rmw_qos_profile_default` | (optional) The rmw qos profile to use to subscribe. |


---

#### `subscribe() [overload 3]`

```cpp
void message_filters::Subscriber<M, NodeType>::subscribe(NodePtr node, std::string &topic, rmw_qos_profile_t qos, agnocast::SubscriptionOptions options)
```

Subscribe to a topic. If this Subscriber is already subscribed to a topic, this function will first unsubscribe.

| Parameter | Description |
|-----------|-------------|
| `node` | The `rclcpp::Node::SharedPtr` to use to subscribe. |
| `topic` | The topic to subscribe to. |
| `qos` | The rmw qos profile to use to subscribe. |
| `options` | The subscription options to use to subscribe. |


---

#### `subscribe() [overload 4]`

```cpp
void message_filters::Subscriber<M, NodeType>::subscribe(NodeType *node, std::string &topic, rmw_qos_profile_t qos, agnocast::SubscriptionOptions options)
```

Subscribe to a topic. If this Subscriber is already subscribed to a topic, this function will first unsubscribe.

| Parameter | Description |
|-----------|-------------|
| `node` | The `rclcpp::Node` to use to subscribe. |
| `topic` | The topic to subscribe to. |
| `qos` | The rmw qos profile to use to subscribe. |
| `options` | The subscription options to use to subscribe. |


---

#### `subscribe() [overload 5]`

```cpp
void message_filters::Subscriber<M, NodeType>::subscribe()
```

Re-subscribe to a topic. Only works if this subscriber has previously been subscribed to a topic.


---

#### `unsubscribe()`

```cpp
void message_filters::Subscriber<M, NodeType>::unsubscribe()
```

Force immediate unsubscription of this subscriber from its topic.


---

#### `getTopic()`

```cpp
std::string message_filters::Subscriber<M, NodeType>::getTopic() const
```

Return the topic name this subscriber is subscribed to.

| | |
|-----------|-------------|
| **Returns** | Topic name string. |


---

#### `getSubscriber()`

```cpp
agnocast::Subscription::SharedPtr message_filters::Subscriber<M, NodeType>::getSubscriber() const
```

Returns the internal `agnocast::Subscription`<M>::SharedPtr object.


---

#### `connectInput()`

```cpp
void message_filters::Subscriber<M, NodeType>::connectInput(F &f)
```

No-op. Provided for compatibility with message_filters::Chain.


---

#### `add()`

```cpp
void message_filters::Subscriber<M, NodeType>::add(EventType &e)
```

No-op. Provided for compatibility with message_filters::Chain.


### `agnocast::message_filters::Synchronizer<Policy>`

**Extends:** `noncopyable`, `Policy`

Synchronizes messages from 2–9 input filters based on a time policy. Drop-in replacement for message_filters::Synchronizer<Policy>. When matching messages are found according to the policy, the registered callback is invoked with one `agnocast::ipc_shared_ptr`<const M> per input.


---

#### `Synchronizer()`

```cpp
message_filters::Synchronizer<Policy>::Synchronizer(F0 &f0, F1 &f1)
```

Construct a synchronizer with 2-9 input filters.


---

#### `Synchronizer() [overload 2]`

```cpp
message_filters::Synchronizer<Policy>::Synchronizer()
```

Construct an unconnected synchronizer. Call connectInput() to connect filters.


---

#### `Synchronizer() [overload 3]`

```cpp
message_filters::Synchronizer<Policy>::Synchronizer(Policy &policy, F0 &f0, F1 &f1)
```

Construct a synchronizer with a policy and 2–9 input filters.

| Parameter | Description |
|-----------|-------------|
| `policy` | Sync policy instance. |
| `f0` | First input filter. |
| `f1` | Second input filter. |


---

#### `Synchronizer() [overload 4]`

```cpp
message_filters::Synchronizer<Policy>::Synchronizer(Policy &policy)
```

Construct a synchronizer with a policy but no input filters.

| Parameter | Description |
|-----------|-------------|
| `policy` | Sync policy instance. |


---

#### `connectInput()`

```cpp
void message_filters::Synchronizer<Policy>::connectInput(F0 &f0, F1 &f1)
```

Connect 2–9 input filters to this synchronizer. Replaces any previous connections.

| Parameter | Description |
|-----------|-------------|
| `f0` | First input filter. |
| `f1` | Second input filter. |


---

#### `registerCallback()`

```cpp
Connection message_filters::Synchronizer<Policy>::registerCallback(C &callback)
```

Register a callback invoked when matching messages are found.

| Parameter | Description |
|-----------|-------------|
| `callback` | Callback to register. |
| | |
| **Returns** | Connection object for disconnecting. |


---

#### `registerCallback() [overload 2]`

```cpp
Connection message_filters::Synchronizer<Policy>::registerCallback(C &callback)
```

Register a const callback.

| Parameter | Description |
|-----------|-------------|
| `callback` | Callback to register. |
| | |
| **Returns** | Connection object. |


---

#### `registerCallback() [overload 3]`

```cpp
Connection message_filters::Synchronizer<Policy>::registerCallback(C &callback, T *t)
```

Register a member function callback.

| Parameter | Description |
|-----------|-------------|
| `callback` | Member function pointer. |
| `t` | Object to call the member function on. |
| | |
| **Returns** | Connection object. |


---

#### `registerCallback() [overload 4]`

```cpp
Connection message_filters::Synchronizer<Policy>::registerCallback(C &callback, T *t)
```

Register a member function callback.

| Parameter | Description |
|-----------|-------------|
| `callback` | Member function pointer. |
| `t` | Object to call the member function on. |
| | |
| **Returns** | Connection object. |


---

#### `setName()`

```cpp
void message_filters::Synchronizer<Policy>::setName(std::string &name)
```

Set the name of this synchronizer (for debugging).

| Parameter | Description |
|-----------|-------------|
| `name` | Name string. |


---

#### `getName()`

```cpp
std::string & message_filters::Synchronizer<Policy>::getName()
```

Return the name of this synchronizer.

| | |
|-----------|-------------|
| **Returns** | Name string. |


---

#### `getPolicy()`

```cpp
Policy * message_filters::Synchronizer<Policy>::getPolicy()
```

Return a pointer to the sync policy. Use this to configure policy parameters after construction (e.g., sync.getPolicy()->setAgePenalty(0.5) ).

| | |
|-----------|-------------|
| **Returns** | Pointer to the policy object. |


### `agnocast::message_filters::PassThrough<M>`

**Extends:** `agnocast::message_filters::SimpleFilter< M >`

Simple passthrough filter. What comes in goes out immediately.


---

#### `PassThrough()`

```cpp
message_filters::PassThrough<M>::PassThrough()
```

Construct an unconnected PassThrough filter.


---

#### `PassThrough() [overload 2]`

```cpp
message_filters::PassThrough<M>::PassThrough(F &f)
```

Construct and connect to an upstream filter.

| Parameter | Description |
|-----------|-------------|
| `f` | Upstream filter to connect. |


---

#### `connectInput()`

```cpp
void message_filters::PassThrough<M>::connectInput(F &f)
```

Connect an upstream filter so its output is forwarded through this PassThrough.

| Parameter | Description |
|-----------|-------------|
| `f` | Upstream filter. |


---

#### `add()`

```cpp
void message_filters::PassThrough<M>::add(MConstPtr &msg)
```

Feed a message to all downstream filters.

| Parameter | Description |
|-----------|-------------|
| `msg` | Message to forward. |


---

#### `add() [overload 2]`

```cpp
void message_filters::PassThrough<M>::add(EventType &evt)
```

Feed a message event to all downstream filters.

| Parameter | Description |
|-----------|-------------|
| `evt` | Event to forward. |


### `agnocast::message_filters::sync_policies::ExactTime<M0, M1, ...>`

**Extends:** `agnocast::message_filters::PolicyBase< M0, M1, NullType, NullType, NullType, NullType, NullType, NullType, NullType >`

Sync policy that matches messages with exactly equal timestamps. Supports 2-9 message types.


---

#### `ExactTime()`

```cpp
message_filters::sync_policies::ExactTime<M0, M1, M2, M3, M4, M5, M6, M7, M8>::ExactTime(uint32_t queue_size)
```

Construct with a queue size.

| Parameter | Description |
|-----------|-------------|
| `queue_size` | Maximum number of messages to buffer per input. |


---

#### `ExactTime() [overload 2]`

```cpp
message_filters::sync_policies::ExactTime<M0, M1, M2, M3, M4, M5, M6, M7, M8>::ExactTime(ExactTime &e)
```

Copy constructor.


---

#### `operator=()`

```cpp
ExactTime & message_filters::sync_policies::ExactTime<M0, M1, M2, M3, M4, M5, M6, M7, M8>::operator=(ExactTime &rhs)
```

Copy assignment.

| | |
|-----------|-------------|
| **Returns** | Reference to *this. |


---

#### `registerDropCallback()`

```cpp
Connection message_filters::sync_policies::ExactTime<M0, M1, M2, M3, M4, M5, M6, M7, M8>::registerDropCallback(C &callback)
```

Register a callback invoked when messages are dropped due to queue overflow or missing matches.

| Parameter | Description |
|-----------|-------------|
| `callback` | Callback to register. |
| | |
| **Returns** | Connection object for disconnecting. |


### `agnocast::message_filters::sync_policies::ApproximateTime<M0, M1, ...>`

**Extends:** `agnocast::message_filters::PolicyBase< M0, M1, NullType, NullType, NullType, NullType, NullType, NullType, NullType >`

Sync policy that matches messages with approximately equal timestamps using cost-based optimization. Supports 2-9 message types.


---

#### `ApproximateTime()`

```cpp
message_filters::sync_policies::ApproximateTime<M0, M1, M2, M3, M4, M5, M6, M7, M8>::ApproximateTime(uint32_t queue_size)
```

Construct with a queue size.

| Parameter | Description |
|-----------|-------------|
| `queue_size` | Maximum number of messages to buffer per input. |


---

#### `ApproximateTime() [overload 2]`

```cpp
message_filters::sync_policies::ApproximateTime<M0, M1, M2, M3, M4, M5, M6, M7, M8>::ApproximateTime(ApproximateTime &e)
```

Copy constructor.


---

#### `operator=()`

```cpp
ApproximateTime & message_filters::sync_policies::ApproximateTime<M0, M1, M2, M3, M4, M5, M6, M7, M8>::operator=(ApproximateTime &rhs)
```

Copy assignment.

| | |
|-----------|-------------|
| **Returns** | Reference to *this. |


---

#### `setAgePenalty()`

```cpp
void message_filters::sync_policies::ApproximateTime<M0, M1, M2, M3, M4, M5, M6, M7, M8>::setAgePenalty(double age_penalty)
```

Set the weight given to message age when computing match cost. Higher values prefer newer messages.

| Parameter | Description |
|-----------|-------------|
| `age_penalty` | Age penalty weight (must be >= 0, default: 0.1). |


---

#### `setInterMessageLowerBound()`

```cpp
void message_filters::sync_policies::ApproximateTime<M0, M1, M2, M3, M4, M5, M6, M7, M8>::setInterMessageLowerBound(int i, rclcpp::Duration lower_bound)
```

Set the minimum expected interval between consecutive messages for a given input.

| Parameter | Description |
|-----------|-------------|
| `i` | Input index (0-based). |
| `lower_bound` | Minimum expected interval (default: 0, auto-estimated). |


---

#### `setMaxIntervalDuration()`

```cpp
void message_filters::sync_policies::ApproximateTime<M0, M1, M2, M3, M4, M5, M6, M7, M8>::setMaxIntervalDuration(rclcpp::Duration max_interval_duration)
```

Set the maximum allowed time difference between matched messages.

| Parameter | Description |
|-----------|-------------|
| `max_interval_duration` | Maximum interval (default: no limit). |

---

## Full Example

```cpp
#include "agnocast/agnocast.hpp"

using MsgA = sensor_msgs::msg::Image;
using MsgB = sensor_msgs::msg::CameraInfo;
using Policy = agnocast::message_filters::sync_policies::ExactTime<MsgA, MsgB>;

class MySyncNode : public rclcpp::Node {
  agnocast::message_filters::Subscriber<MsgA> sub_a_;
  agnocast::message_filters::Subscriber<MsgB> sub_b_;
  agnocast::message_filters::Synchronizer<Policy> sync_;

  void callback(const agnocast::ipc_shared_ptr<const MsgA> & a,
                const agnocast::ipc_shared_ptr<const MsgB> & b) {
    // Process synchronized messages
  }

public:
  MySyncNode() : Node("sync_node"),
    sub_a_(this, "/image"),
    sub_b_(this, "/camera_info"),
    sync_(Policy(10), sub_a_, sub_b_) {
    sync_.registerCallback(&MySyncNode::callback, this);
  }
};
```

