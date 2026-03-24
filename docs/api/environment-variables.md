
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

Controls the Agnocast–ROS 2 bridge mode for interoperability with standard ROS 2 nodes.

| Value | Description |
|-------|-------------|
| `0` or `off` | Bridge disabled. Agnocast topics are not visible to ROS 2 nodes. |
| `1` or `standard` | **Standard mode (default).** Each Agnocast process runs its own bridge manager. |
| `2` or `performance` | **Performance mode.** A single global bridge manager handles all bridging with pre-compiled plugins for lower overhead. |

Case-insensitive. Falls back to Standard mode with a warning if an unknown value is given.

```bash
export AGNOCAST_BRIDGE_MODE=standard
```

---

#### `AGNOCAST_BRIDGE_PLUGINS_PATH`

**Performance mode only.** Colon-separated list of additional search paths for bridge plugin shared libraries (`.so` files). If not set, plugins are searched in the default package install location.

```bash
export AGNOCAST_BRIDGE_PLUGINS_PATH=/opt/my_plugins:/home/user/plugins
```

