# Constraints & Differences from ROS 2 `domain_bridge`

The Agnocast domain bridge reuses the ROS 2 [`domain_bridge`](https://github.com/ros2/domain_bridge) YAML format, but it behaves differently in several ways.

## Functional differences

| | ROS 2 `domain_bridge` | Agnocast domain bridge |
| --- | --- | --- |
| Topic renaming (`remap`) | Supported | **Not supported** — the topic must have the same name in both domains |
| When a rule can be registered | Any time (dynamic relay node) | **Before any publisher or subscriber for that topic exists** in either domain — otherwise rejected |
| Domains per topic | Multiple | **One domain pair** per topic (no fan-out to a third domain) |
| Direction (`bidirectional` / `reversed`) | Two-way per topic | **One-directional** — `bidirectional` / `reversed` are ignored; register the reverse rule separately |
| Per-topic QoS | Can be overridden | **Not supported** — each endpoint keeps its own QoS (the `type` and QoS fields in the config are ignored) |
| Services | Bridged | **Pub/sub only** |

## Scope

- **Zero copy only within one IPC namespace** (same machine) and only between **Agnocast endpoints**. Cross-ECU, cross-IPC-namespace, or Agnocast ↔ ROS 2 traffic goes through the [Agnocast–ROS 2 Bridge](../migration-guide/bridge.md) over DDS, with a copy. See [Limitations](../index.md#limitations).
- **Performance mode only.**

## Behavior to be aware of

- **QoS history window.** When a rule is active, heavy publishing in the source domain can shrink the effective QoS history window seen within the destination domain, because both domains share one message stream.
- **Duplicate delivery across paths.** If you also bridge the same topic across ECUs through the ROS 2 `domain_bridge`, a subscriber can receive the message twice — once from each path. Don't bridge the same topic by both mechanisms within the same namespace.
- **Shared endpoint capacity.** The two bridged domains share one per-topic publisher / subscriber capacity limit, so their combined endpoint count counts against that single limit.
