
# Environment Variables

<!-- Auto-generated — do not edit. Regenerate with: doxygen Doxyfile && python3 generate_api_reference.py -->

These environment variables configure Agnocast runtime behavior.

---

#### `LD_PRELOAD`

**Required.** Must include `libagnocast_heaphook.so` to route heap allocations to shared memory. Agnocast validates this at startup and exits with an error if missing.

The heaphook replaces the following allocation/deallocation functions: `malloc`, `free`, `calloc`, `realloc`, `posix_memalign`, `aligned_alloc`, and `memalign`. `valloc` and `pvalloc` are intercepted but not supported; calling them aborts the process.

Set it per-node in a launch file. Prepend `libagnocast_heaphook.so` to the existing `LD_PRELOAD` value (the `$(env LD_PRELOAD '')` part) so that libraries already listed there are preserved:

```xml
<node pkg="my_package" exec="my_node" name="my_node" output="screen">
    <env name="LD_PRELOAD" value="libagnocast_heaphook.so:$(env LD_PRELOAD '')" />
</node>
```

For a component container, set it on the `<node_container>` element. Use the `agnocast_components` package; the `agnocast_component_container` executable in the `agnocastlib` package is deprecated:

```xml
<node_container pkg="agnocast_components" exec="agnocast_component_container" name="my_container">
    <env name="LD_PRELOAD" value="libagnocast_heaphook.so:$(env LD_PRELOAD '')" />
</node_container>
```

In a Python launch file, use `additional_env`:

```python
import os

container = ComposableNodeContainer(
    ...,
    additional_env={
        'LD_PRELOAD': f"libagnocast_heaphook.so:{os.getenv('LD_PRELOAD', '')}",
    },
)
```

!!! warning
    Applications that hook the same allocation/deallocation functions cannot be used together with Agnocast.

---

#### `AGNOCAST_BRIDGE_MODE`

Enables or disables the Agnocast–ROS 2 Bridge for interoperability with standard ROS 2 nodes.

| Value | Description |
|-------|-------------|
| `0` or `off` | Bridge disabled. Agnocast and ROS 2 nodes cannot communicate. |
| `on` | **Bridge enabled (default).** One bridge manager per IPC namespace. |

Case-insensitive. Falls back to `on` with a warning if an unknown value is given. `1` / `standard` and `2` / `performance` are accepted for backward compatibility but are deprecated aliases for `on`.

```bash
export AGNOCAST_BRIDGE_MODE=on
```

---

#### `AGNOCAST_BRIDGE_NODE_NAME_SUFFIX`

Gives the bridge manager node a stable name. By default the node is named `agnocast_bridge_node_performance_<ipc_ns_inode>_<pid>`, which changes on every launch, so tools that reference node names in static configuration files (e.g. CIE thread configuration) cannot match it. When this variable is set, the node is named `agnocast_bridge_node_performance_<suffix>` instead.

| Value | Node name |
|-------|-----------|
| unset or empty | `agnocast_bridge_node_performance_<ipc_ns_inode>_<pid>` (default, unique per launch) |
| `<suffix>` | `agnocast_bridge_node_performance_<suffix>` |

The variable carries only the suffix so that the `agnocast_bridge_node_` prefix, which the `ros2 agnocast` CLI and other tools rely on, is preserved. `-` and `.` (common in container names) are replaced with `_`. If the value contains any other character not allowed in ROS 2 node names, or the resulting node name would exceed the maximum node name length (255 characters), the value is ignored with a warning and the default naming is used, so a misconfigured value never prevents the bridge from starting.

The deployment configuration is responsible for injecting a value that is unique within the ROS 2 domain, such as the container name (combined with an ECU name in multi-ECU setups):

```yaml
# docker-compose.yaml
services:
  planning:
    environment:
      - AGNOCAST_BRIDGE_NODE_NAME_SUFFIX=main_planning  # -> /agnocast_bridge_node_performance_main_planning
```

---

#### `AGNOCAST_BRIDGE_PLUGINS_PATH`

Colon-separated list of additional search paths for bridge plugin shared libraries (`.so` files). If not set, plugins are searched in the default package install location.

```bash
export AGNOCAST_BRIDGE_PLUGINS_PATH=/opt/my_plugins:/home/user/plugins
```

---

#### `AGNOCAST_DOMAIN_BRIDGE_CONFIG`

Default path to a [`domain_bridge` rule file](../domain-bridge/configuration.md) for the standalone `register_domain_bridge` tool: `ros2 run ros2agnocast_discovery_agent register_domain_bridge` reads it when `--config` is not given. Register the rules **before** the nodes that use those topics start.

```bash
export AGNOCAST_DOMAIN_BRIDGE_CONFIG=/path/to/domain_bridge.yaml
```

