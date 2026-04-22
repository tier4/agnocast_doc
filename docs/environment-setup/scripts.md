# Scripts

Agnocast ships several convenience scripts under the [`scripts/` directory](https://github.com/autowarefoundation/agnocast/tree/main/scripts) of the repository. The tables below cover user-facing scripts. Developer- and maintainer-only scripts (build, test, lint, release) are documented in [`scripts/README.md`](https://github.com/autowarefoundation/agnocast/blob/main/scripts/README.md) in the repository.

All scripts are intended to be invoked from the repository root after sourcing the ROS 2 environment and, where applicable, the local workspace (`source install/setup.bash`).

## Setup and runtime configuration

Neither script requires `agnocast.ko` to be loaded or `libagnocast_heaphook.so` to be available — they only configure the host system.

| Script | Purpose |
|---|---|
| `dds_config.bash` | Apply CycloneDDS runtime settings (`net.core.rmem_max`, loopback multicast) required for Agnocast over CycloneDDS. Guarded by `/tmp/cycloneDDS_configured` so it runs only once per boot. |
| `setup_thread_configurator.bash` | Grant `CAP_SYS_NICE` to `thread_configurator_node` and register library paths in `/etc/ld.so.conf.d/agnocast-cie.conf`. Automates the manual steps described in [CallbackIsolatedExecutor → Integration Guide, Step 2](../callback-isolated-executor/integration-guide.md#step-2-set-up-the-thread-configurator). |

## Kernel module management

| Script | Purpose |
|---|---|
| `switch_kmod.bash` | Swap the host's `agnocast-kmod-v<ver>` to another version. For container-based setups where the heaphook travels with the container image and only the host-side kmod needs to be replaced independently. See [Running in Containers → Swapping the host kernel module](../tips/containers.md#swapping-the-host-kernel-module) for details. |

## Sample application launchers

Each `sample_application/run_*.bash` script is a thin wrapper that runs `source install/setup.bash` followed by `ros2 launch agnocast_sample_application <name>.launch.xml`. All launch files set `LD_PRELOAD=libagnocast_heaphook.so` automatically, so every sample below requires both `agnocast.ko` to be loaded and `libagnocast_heaphook.so` to be available (via apt or a local source build).

**Samples inheriting from `rclcpp::Node`:**

| Script | Launch file |
|---|---|
| `run_talker.bash` | `talker.launch.xml` |
| `run_listener.bash` | `listener.launch.xml` |
| `run_cie_talker.bash` | `cie_talker.launch.xml` (`CallbackIsolatedAgnocastExecutor`) |
| `run_cie_listener.bash` | `cie_listener.launch.xml` (`CallbackIsolatedAgnocastExecutor`) |
| `run_client.bash` | `client.launch.xml` (service client) |
| `run_server.bash` | `server.launch.xml` (service server) |

**Samples inheriting from `agnocast::Node` (instead of `rclcpp::Node`):**

| Script | Launch file |
|---|---|
| `run_no_rclcpp_talker.bash` | `no_rclcpp_talker.launch.xml` |
| `run_no_rclcpp_listener.bash` | `no_rclcpp_listener.launch.xml` |
| `run_no_rclcpp_take_listener.bash` | `no_rclcpp_take_listener.launch.xml` (polling-style subscription) |
| `run_no_rclcpp_pubsub.bash` | `no_rclcpp_pubsub.launch.xml` |
| `run_no_rclcpp_client.bash` | `no_rclcpp_client.launch.xml` |
| `run_no_rclcpp_server.bash` | `no_rclcpp_server.launch.xml` |
| `run_sim_time_timer.bash` | `sim_time_timer.launch.xml` (simulation time) |
