
# API Reference

<!-- Auto-generated — do not edit. Regenerate with: doxygen Doxyfile && python3 generate_api_reference.py -->

!!! info "Stability Guarantee"
    All API signatures documented here are marked with `AGNOCAST_PUBLIC` in the source code.
    These signatures are **stable** and will not break backward compatibility unless the
    **major version** is incremented. See the [versioning rules](../environment-setup/index.md)
    for details.

    **Exception:** The [Service](service.md) and [Client](client.md) APIs are **experimental**.
    Their signatures may introduce breaking changes without a major version increment.

| Section | Description |
|---------|-------------|
| [Free Functions (Stage 1)](free-functions.md) | Free functions for use with `rclcpp::Node` (`create_publisher`, `create_subscription`, etc.). |
| [Type Aliases](type-aliases.md) | User-facing type aliases (`Publisher`, `Subscription`, `PollingSubscriber`, etc.). |
| [`agnocast::Node`](node.md) | Agnocast-only node. |
| [`agnocast::Publisher<MessageT>`](publisher.md) | Zero-copy publisher that allocates messages in shared memory. |
| [`agnocast::Subscription<MessageT>`](subscription.md) | Event-driven subscription that invokes a callback on each new message. |
| [`agnocast::TakeSubscription<MessageT>`](takesubscription.md) | Polling-based subscription that retrieves messages on demand via take(). |
| [`agnocast::PollingSubscriber<MessageT>`](pollingsubscriber.md) | Polling subscription that retrieves messages on demand. |
| [`agnocast::ipc_shared_ptr<T>`](ipc_shared_ptr.md) | Smart pointer for zero-copy IPC message sharing between publishers and subscribers. |
| [`agnocast::Client<ServiceT>`](client.md) | Service client for zero-copy Agnocast service communication. |
| [`agnocast::Service<ServiceT>`](service.md) |  |
| [`agnocast::TimerBase`](timerbase.md) | Base class for Agnocast timers providing periodic callback execution. |
| [`agnocast::GenericTimer<FunctorT>`](generictimer.md) | Timer that fires periodically using a user-provided clock. |
| [`agnocast::WallTimer<FunctorT>`](walltimer.md) | Timer that uses a steady (wall) clock. |
| [Executors](executors.md) | Single-threaded, multi-threaded, and callback-isolated executors for Stage 1 and Stage 2. |
| [Options](options.md) | `PublisherOptions` and `SubscriptionOptions` configuration structs. |
| [Environment Variables](environment-variables.md) | `LD_PRELOAD`, `AGNOCAST_BRIDGE_MODE`, and other runtime configuration variables. |
| [Message Filters](message-filters.md) | Synchronizer, Subscriber filter, PassThrough, and time sync policies. |

