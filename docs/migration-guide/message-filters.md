# Message Filters

Agnocast provides message synchronization filters compatible with the ROS 2 `message_filters` API. These allow you to synchronize messages from multiple Agnocast topics based on their timestamps.

## Feature Support Status

| Component | Support |
|-----------|---------|
| Synchronizer (2–9 inputs) | Supported |
| ExactTime policy | Supported |
| ApproximateTime policy | Supported |
| ApproximateEpsilonTime policy | Not supported |
| Subscriber filter | Supported |
| PassThrough filter | Supported |
| Cache | Not supported |
| Chain | Not supported |

Synchronizing standard ROS 2 subscriptions (`std::shared_ptr<const M>`) and Agnocast subscriptions (`agnocast::ipc_shared_ptr<const M>`) within the same `Synchronizer` is not supported — all inputs must be Agnocast subscriptions.

## Prerequisites

Both sync policies extract an `rclcpp::Time` from each message. You must specialize the `message_filters::message_traits::TimeStamp` trait for every message type used with the `Synchronizer`. Messages with a `header.stamp` field (e.g., `sensor_msgs::msg::Image`, `geometry_msgs::msg::PoseStamped`) are supported out of the box.

## Migrating a Synchronizer

### Before (rclcpp message_filters)

```cpp
#include <message_filters/subscriber.h>
#include <message_filters/synchronizer.h>
#include <message_filters/sync_policies/exact_time.h>

using MsgA = sensor_msgs::msg::Image;
using MsgB = sensor_msgs::msg::CameraInfo;
using SyncPolicy = message_filters::sync_policies::ExactTime<MsgA, MsgB>;

class MySyncNode : public rclcpp::Node
{
  message_filters::Subscriber<MsgA> sub_a_;
  message_filters::Subscriber<MsgB> sub_b_;
  message_filters::Synchronizer<SyncPolicy> sync_;

  void callback(
    const MsgA::ConstSharedPtr & a,
    const MsgB::ConstSharedPtr & b)
  {
    // Process synchronized messages
  }

public:
  MySyncNode() : Node("sync_node"),
    sub_a_(this, "/image"),
    sub_b_(this, "/camera_info"),
    sync_(SyncPolicy(10), sub_a_, sub_b_)
  {
    sync_.registerCallback(&MySyncNode::callback, this);
  }
};
```

### After (Agnocast Stage 1)

```cpp
#include "agnocast/agnocast.hpp"                                       // (1)

using MsgA = sensor_msgs::msg::Image;
using MsgB = sensor_msgs::msg::CameraInfo;
using SyncPolicy =
  agnocast::message_filters::sync_policies::ExactTime<MsgA, MsgB>;    // (2)

class MySyncNode : public rclcpp::Node
{
  agnocast::message_filters::Subscriber<MsgA> sub_a_;                  // (3)
  agnocast::message_filters::Subscriber<MsgB> sub_b_;                  // (3)
  agnocast::message_filters::Synchronizer<SyncPolicy> sync_;           // (4)

  void callback(
    const agnocast::ipc_shared_ptr<const MsgA> & a,                   // (5)
    const agnocast::ipc_shared_ptr<const MsgB> & b)
  {
    // Process synchronized messages
  }

public:
  MySyncNode() : Node("sync_node"),
    sub_a_(this, "/image"),
    sub_b_(this, "/camera_info"),
    sync_(SyncPolicy(10), sub_a_, sub_b_)
  {
    sync_.registerCallback(&MySyncNode::callback, this);
  }
};
```

Key changes:

1. Include changes to `agnocast/agnocast.hpp`
2. Sync policy namespace changes to `agnocast::message_filters::sync_policies`
3. `message_filters::Subscriber` → `agnocast::message_filters::Subscriber`
4. `message_filters::Synchronizer` → `agnocast::message_filters::Synchronizer`
5. Callback receives `agnocast::ipc_shared_ptr<const T>` instead of `T::ConstSharedPtr`

### After (Agnocast Stage 2)

```cpp
#include "agnocast/agnocast.hpp"

using MsgA = sensor_msgs::msg::Image;
using MsgB = sensor_msgs::msg::CameraInfo;
using SyncPolicy =
  agnocast::message_filters::sync_policies::ExactTime<MsgA, MsgB>;

class MySyncNode : public agnocast::Node                               // (1)
{
  agnocast::message_filters::Subscriber<MsgA, agnocast::Node> sub_a_;    // (2)
  agnocast::message_filters::Subscriber<MsgB, agnocast::Node> sub_b_;
  agnocast::message_filters::Synchronizer<SyncPolicy> sync_;

  void callback(
    const agnocast::ipc_shared_ptr<const MsgA> & a,
    const agnocast::ipc_shared_ptr<const MsgB> & b)
  {
    // Process synchronized messages
  }

public:
  MySyncNode() : Node("sync_node"),
    sub_a_(this, "/image"),
    sub_b_(this, "/camera_info"),
    sync_(SyncPolicy(10), sub_a_, sub_b_)
  {
    sync_.registerCallback(&MySyncNode::callback, this);
  }
};
```

Additional changes from Stage 1:

1. Base class changes to `agnocast::Node`
2. `Subscriber` takes the node type as its second template argument
   (`Subscriber<MsgA, agnocast::Node>`); it defaults to `rclcpp::Node`, which
   `agnocast::Node` does not derive from

## ExactTime Policy

For `ExactTime`, the `queue_size` constructor argument is the maximum number of **incomplete message sets** to buffer. When exceeded, the oldest sets are dropped.

You can register a drop callback that is invoked whenever incomplete sets are discarded. It has the same signature as the main callback:

```cpp
sync.getPolicy()->registerDropCallback(&MySyncNode::dropCallback, this);
```

## ApproximateTime Policy

The migration steps are the same as ExactTime — replace `ExactTime` with `ApproximateTime` in the policy type:

```cpp
using SyncPolicy =
  agnocast::message_filters::sync_policies::ApproximateTime<MsgA, MsgB>;
```

All parameter APIs from rclcpp's `message_filters::sync_policies::ApproximateTime` are supported with identical signatures:

```cpp
SyncPolicy policy(10);  // queue size
policy.setMaxIntervalDuration(rclcpp::Duration(0, 100'000'000));  // 100ms max
policy.setAgePenalty(0.5);
policy.setInterMessageLowerBound(0, rclcpp::Duration(0, 30'000'000));  // 30ms for input 0

agnocast::message_filters::Synchronizer<SyncPolicy> sync(policy, sub_a_, sub_b_);
```

| Method | Description | Default |
|--------|-------------|---------|
| `setMaxIntervalDuration(duration)` | Maximum time difference between matched messages | No limit |
| `setAgePenalty(double)` | Weight given to message age in matching (must be >= 0) | 0.1 |
| `setInterMessageLowerBound(i, duration)` | Minimum expected interval between messages for input `i` | 0 (auto-estimated) |

Unlike `ExactTime`, the `queue_size` constructor argument limits the number of buffered messages **per topic** (not message sets). It must be greater than 0; a value of at least 2 is recommended, since a queue size of 1 tends to drop many messages.

`ApproximateTime` does not support drop callbacks.

!!! note
    The policy logs a one-time warning if messages arrive out of timestamp order, or if the actual interval between messages is smaller than the bound declared with `setInterMessageLowerBound()`.

## Callback Signatures

The synchronized callback can use any of these parameter types, and they can be mixed:

```cpp
// By const reference (recommended)
void cb(const agnocast::ipc_shared_ptr<MsgA const> & a,
        const agnocast::ipc_shared_ptr<MsgB const> & b);

// By value
void cb(agnocast::ipc_shared_ptr<MsgA const> a,
        agnocast::ipc_shared_ptr<MsgB const> b);

// As MessageEvent (provides receipt time metadata)
void cb(const agnocast::message_filters::MessageEvent<MsgA const> & a,
        const agnocast::message_filters::MessageEvent<MsgB const> & b);
```

Callbacks can be registered as:

```cpp
// Free function
sync.registerCallback(myFreeFunction);

// Bound via std::bind
sync.registerCallback(std::bind(&MyClass::callback, this, std::placeholders::_1, std::placeholders::_2));

// Member function pointer (recommended for class methods)
sync.registerCallback(&MyClass::callback, this);
```

## Migrating a PassThrough Filter

`PassThrough` forwards messages without filtering — useful when you already have a subscription and want to feed it into a Synchronizer. The API is identical to rclcpp's `message_filters::PassThrough`.

### Before (rclcpp message_filters)

```cpp
message_filters::PassThrough<MsgType> pass_through;

// Feed messages manually
pass_through.add(message);  // message is MsgType::ConstSharedPtr
```

### After (Agnocast)

```cpp
agnocast::message_filters::PassThrough<MsgType> pass_through;          // (1)

// Feed messages manually
pass_through.add(message);  // message is agnocast::ipc_shared_ptr<const MsgType>  // (2)
```

Key changes:

1. `message_filters::PassThrough` → `agnocast::message_filters::PassThrough`
2. `add()` takes `agnocast::ipc_shared_ptr<const T>` instead of `T::ConstSharedPtr`
