
# Environment Variables

<!-- Auto-generated — do not edit. Regenerate with: doxygen Doxyfile && python3 generate_api_reference.py -->

These environment variables configure Agnocast runtime behavior.

---

#### `LD_PRELOAD`

**Required.** Must include `libagnocast_heaphook.so` to route heap allocations to shared memory. Agnocast validates this at startup and exits with an error if missing.

Set it per-node in a launch file:

```xml
<node pkg="my_package" exec="my_node" name="my_node" output="screen">
    <env name="LD_PRELOAD" value="libagnocast_heaphook.so:$(env LD_PRELOAD '')" />
</node>
```

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

