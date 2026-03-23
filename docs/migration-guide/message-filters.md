# Message Filters

Agnocast provides message synchronization filters compatible with the ROS 2 `message_filters` API. These allow you to synchronize messages from multiple Agnocast topics based on their timestamps.

| Component | Support |
|-----------|---------|
| Synchronizer (2–9 inputs) | Supported |
| ExactTime policy | Supported |
| ApproximateTime policy | Supported |
| Subscriber filter | Supported |
| PassThrough filter | Supported |
| Cache | Not supported |
| Chain | Not supported |

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
    const agnocast::ipc_shared_ptr<MsgA> & a,                         // (5)
    const agnocast::ipc_shared_ptr<MsgB> & b)
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
  agnocast::message_filters::Subscriber<MsgA> sub_a_;
  agnocast::message_filters::Subscriber<MsgB> sub_b_;
  agnocast::message_filters::Synchronizer<SyncPolicy> sync_;

  void callback(
    const agnocast::ipc_shared_ptr<MsgA> & a,
    const agnocast::ipc_shared_ptr<MsgB> & b)
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

Additional change from Stage 1:

1. Base class changes to `agnocast::Node`

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
