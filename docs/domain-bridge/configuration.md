# Configuring the Domain Bridge

You declare which topics to bridge, and between which domains, in a YAML file. Agnocast reuses the [ROS 2 `domain_bridge`](https://github.com/ros2/domain_bridge) file format, so existing config is familiar — Agnocast simply ignores the fields it does not support (see [Constraints](constraints.md)).

A small standalone tool, `register_domain_bridge`, reads this file and registers each rule with the kernel module. Run it once, **before the nodes that use those topics start**.

## Register rules before your nodes start

This is the most important rule to get right. A bridge rule can only be registered for a topic that has **no publisher or subscriber yet in either domain**. If an endpoint for the topic already exists when the rule is applied, the registration is **rejected**.

So `register_domain_bridge` must run — and register the rules — **before** the nodes that use those topics come up. The discovery agent does **not** register rules; this is a separate, one-time step.

!!! note "Boot-time loading is planned"
    For now you arrange this ordering yourself (see [Applying the config](#applying-the-config)). Loading bridge rules automatically at module-load time, before any application starts, is on the roadmap.

## File format

```yaml
# Default direction for every topic below. Per-topic values override these.
from_domain: 1
to_domain: 2

topics:
  # Bridge /chatter from domain 1 to domain 2 (uses the defaults above).
  chatter:

  # Override the direction for a single topic.
  image:
    from_domain: 3
    to_domain: 4
```

- The map key (`chatter`, `image`) is the topic name. It is the **same name in both domains** — Agnocast does not rename topics.
- `from_domain` / `to_domain` are `ROS_DOMAIN_ID` values. Give them at the top level as defaults, per topic, or both.
- A topic with no resolved `from_domain` / `to_domain` (no default and no override) is skipped.
- The ROS 2 `type` field is accepted but ignored — matching is type-independent.

Each rule is one-directional (`from_domain` → `to_domain`). ROS 2's `bidirectional` / `reversed` options are ignored — to bridge both ways, register the reverse `to_domain` → `from_domain` rule as well (a separate config or run, since one `topics:` map can't repeat a topic name).

## Applying the config

Run `register_domain_bridge`, pointing it at your file:

```bash
ros2 run ros2agnocast_discovery_agent register_domain_bridge --config /path/to/domain_bridge.yaml
# or set AGNOCAST_DOMAIN_BRIDGE_CONFIG instead of passing --config
```

It registers every rule and exits. It is idempotent (re-running is safe) and exits non-zero if any rule is rejected — so a node that came up too early fails loudly instead of silently leaving a topic unbridged.

For production, run it from a boot step ordered **after** the kernel module is loaded and **before** your application nodes — for example a systemd one-shot. The `ros2agnocast_discovery_agent` package ships a reference unit (`systemd/agnocast-domain-bridge.service.example`) that shows this ordering.
