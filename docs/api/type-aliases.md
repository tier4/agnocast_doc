
# Type Aliases

<!-- Auto-generated — do not edit. Regenerate with: doxygen Doxyfile && python3 generate_api_reference.py -->

These are the user-facing type aliases. Use these types instead of the internal `Basic*` templates when declaring variables.

| Alias | Defined As | Description |
|-------|-----------|-------------|
| `agnocast::Publisher<MessageT>` | `agnocast::BasicPublisher<MessageT>` | The user-facing Agnocast publisher type. Alias for BasicPublisher<MessageT> . Use this type (not BasicPublisher directly) when declaring publisher variables. |
| `agnocast::Subscription<MessageT>` | `agnocast::BasicSubscription<MessageT>` | The user-facing event-driven subscription type. Alias for BasicSubscription<MessageT>. Use this type (not BasicSubscription directly) when declaring subscription variables. |
| `agnocast::TakeSubscription<MessageT>` | `agnocast::BasicTakeSubscription<MessageT>` | The user-facing polling take-subscription type. Alias for BasicTakeSubscription<MessageT>. Use this type (not BasicTakeSubscription directly) when declaring take-subscription variables. |
| `agnocast::PollingSubscriber<MessageT>` | `agnocast::BasicPollingSubscriber<MessageT>` | The user-facing polling subscriber type. Alias for BasicPollingSubscriber<MessageT>. Use this type (not BasicPollingSubscriber directly) when declaring polling subscriber variables. |
| `agnocast::Service<MessageT>` | `BasicService<ServiceT, RosToAgnocastServiceRequestPolicy>` | The user-facing Agnocast service server. Alias for BasicService<ServiceT> . Use this type (not BasicService directly) when declaring service server variables. The service/client API is experimental and may change in future versions. |

