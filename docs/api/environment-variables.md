
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

#### `AGNOCAST_BRIDGE_PLUGINS_PATH`

Colon-separated list of additional search paths for bridge plugin shared libraries (`.so` files). If not set, plugins are searched in the default package install location.

```bash
export AGNOCAST_BRIDGE_PLUGINS_PATH=/opt/my_plugins:/home/user/plugins
```

