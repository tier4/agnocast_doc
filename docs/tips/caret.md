# CARET Support

[CARET](https://github.com/tier4/caret) is a performance analysis tool for ROS 2 applications. It traces callback execution, message passing latency, and scheduling behavior using LTTng tracepoints.

Agnocast provides its own LTTng tracepoints under the `agnocast` provider, designed to be compatible with CARET. This means that after migrating from rclcpp to Agnocast, you can continue to use CARET for performance analysis without any changes to your tracing workflow.

## Supported Tracepoints

| Tracepoint | Description |
|------------|-------------|
| `agnocast_init` | Agnocast context initialization |
| `agnocast_node_init` | Node creation |
| `agnocast_publisher_init` | Publisher creation |
| `agnocast_subscription_init` | Subscription creation |
| `agnocast_timer_init` | Timer creation |
| `agnocast_publish` | Message publish |
| `agnocast_take` | Message take (polling subscription) |
| `agnocast_create_callable` | Subscription callback ready for execution |
| `agnocast_create_timer_callable` | Timer callback ready for execution |
| `agnocast_callable_start` | Callback execution start |
| `agnocast_callable_end` | Callback execution end |
| `agnocast_construct_executor` | Executor creation |
| `agnocast_add_callback_group` | Callback group added to executor |
