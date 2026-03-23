# Integration Guide

## Overview

1. **Switch the executor** in your application code or launch file
2. **Set up the thread configurator** (one-time system configuration)
3. **Generate a YAML template** by running the configurator in `--prerun` mode
4. **Edit the YAML** to assign scheduling policies, priorities, and CPU affinities
5. **Launch the configurator** with your config file, then start your application

See the [Tutorial](tutorial.md) for a concrete walkthrough with a sample application.

## Step 1: Switch the Executor

### Nodes with a `main` function

Replace the executor:

**Before:**

```cpp
rclcpp::executors::SingleThreadedExecutor executor;
```

**After:**

```cpp
agnocast::CallbackIsolatedAgnocastExecutor executor;
```

### Composable Nodes

Use `agnocast_component_container_cie` in your launch file:

```xml
<node_container pkg="agnocast_components" exec="agnocast_component_container_cie"
                name="my_container" namespace="" output="screen">
    <!-- LD_PRELOAD is only needed when using Agnocast pub/sub -->

    <composable_node pkg="my_package" plugin="MyNode"
                     name="my_node" namespace="">
    </composable_node>
</node_container>
```

Or via CMake registration:

```cmake
agnocast_components_register_node(
  my_component
  PLUGIN "MyNode"
  EXECUTABLE my_node
  EXECUTOR CallbackIsolatedAgnocastExecutor
)
```

For multiple ROS domains, use the `--domains` option:

```xml
<node_container pkg="agnocast_components" exec="agnocast_component_container_cie"
                name="my_container" namespace="" output="screen"
                args="--domains 0 1">
    <!-- components -->
</node_container>
```

## Step 2: Set Up the Thread Configurator

### Grant capabilities

```bash
sudo setcap cap_sys_nice=eip $(readlink -f $(ros2 pkg prefix agnocast_cie_thread_configurator)/lib/agnocast_cie_thread_configurator/thread_configurator_node)
```

!!! note
    `setcap` does not work on symlinks. `readlink -f` resolves to the actual binary, which is needed when using `colcon build --symlink-install`.

### Configure library paths

After `setcap`, the dynamic linker ignores `LD_LIBRARY_PATH` for security. Register the paths explicitly:

Create `/etc/ld.so.conf.d/agnocast-cie.conf` with all directories that contain libraries needed by the thread configurator. For example:

```bash
echo "/opt/ros/$ROS_DISTRO/lib
/opt/ros/$ROS_DISTRO/lib/$(dpkg-architecture -qDEB_HOST_MULTIARCH)
$(ros2 pkg prefix agnocast_cie_config_msgs)/lib" | sudo tee /etc/ld.so.conf.d/agnocast-cie.conf
```

Apply:

```bash
sudo ldconfig
```

### Kernel boot parameter (SCHED_DEADLINE only)

If using `SCHED_DEADLINE`, CPU affinity requires cgroup v1:

```
GRUB_CMDLINE_LINUX_DEFAULT="... systemd.unified_cgroup_hierarchy=0 ..."
```

```bash
sudo update-grub
sudo reboot
```

!!! note
    `SCHED_DEADLINE` cannot be set via capabilities alone — the configurator must be run as **root**.

## Step 3: Generate a YAML Template

Start the prerun node **before** launching your application:

```bash
# Terminal 1: start the prerun node first
ros2 run agnocast_cie_thread_configurator thread_configurator_node --prerun

# Terminal 2: then launch your application
ros2 launch your_package your_launch.xml
```

Once all CallbackGroups are discovered, press Ctrl+C in the prerun terminal. A `template.yaml` is created in the current directory.

## Step 4: Edit the YAML

Edit the template to assign scheduling parameters. See the [YAML Specification](yaml-specification.md) for all options.

For callback groups that don't need configuration, delete the entry or leave the defaults.

## Step 5: Launch with Configuration

Start the configurator **before** the target application:

```bash
ros2 run agnocast_cie_thread_configurator thread_configurator_node --config-file /path/to/config.yaml
```

Then launch your application. The configurator applies scheduling parameters as CallbackGroups register.

!!! note
    The configurator automatically subscribes to all ROS domains referenced by `domain_id` in the YAML configuration. For `--prerun` mode, use the `--domains` option to specify which domains to discover.
