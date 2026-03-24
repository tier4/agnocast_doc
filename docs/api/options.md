
# Options

<!-- Auto-generated — do not edit. Regenerate with: doxygen Doxyfile && python3 generate_api_reference.py -->


### `agnocast::PublisherOptions`

Options for configuring an Agnocast publisher.

| Type | Field | Default | Description |
|------|-------|---------|-------------|
| `rclcpp::QosOverridingOptions` | `qos_overriding_options` | `{}` | QoS parameter override options (same semantics as rclcpp). |


### `agnocast::SubscriptionOptions`

Options for configuring an Agnocast subscription.

| Type | Field | Default | Description |
|------|-------|---------|-------------|
| `rclcpp::CallbackGroup::SharedPtr` | `callback_group` | `nullptr` | Callback group for the subscription (nullptr = default group). |
| `bool` | `ignore_local_publications` | `false` | If true, messages from publishers in the same process are ignored. |
| `rclcpp::QosOverridingOptions` | `qos_overriding_options` | `{}` | QoS parameter override options (same semantics as rclcpp). |

