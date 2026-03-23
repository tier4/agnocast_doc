# Non-ROS Threads

The thread configurator can also manage scheduling for threads that are not part of any ROS 2 executor — for example, sensor driver threads or custom worker threads.

## Usage

Use `agnocast_cie_thread_configurator::spawn_non_ros2_thread` instead of `std::thread` to create the thread. This function automatically reports the thread's ID to the configurator so that scheduling parameters can be applied.

```cpp
#include "agnocast_cie_thread_configurator/cie_thread_configurator.hpp"

// Instead of:
//   std::thread t(my_worker_function, arg1, arg2);

// Use:
std::thread t = agnocast_cie_thread_configurator::spawn_non_ros2_thread(
  "my_worker",        // unique thread name (must match YAML config)
  my_worker_function,
  arg1, arg2);
```

The `thread_name` must be unique among all threads managed by the configurator, and must match the `name` field in the YAML configuration.

## CMake

Add `agnocast_cie_thread_configurator` as a dependency:

```cmake
find_package(agnocast_cie_thread_configurator REQUIRED)
ament_target_dependencies(your_target agnocast_cie_thread_configurator)
```

## YAML Configuration

Configure non-ROS threads under the `non_ros_threads` section:

```yaml
non_ros_threads:
  - name: my_worker
    policy: SCHED_FIFO
    priority: 85
    affinity: [3]
```

The fields are the same as `callback_groups` except `name` is used instead of `id`. All scheduling policies including `SCHED_DEADLINE` are supported. See the [YAML Specification](yaml-specification.md#non_ros_threads) for details.

## Prerun Mode

Non-ROS threads are also discovered by `--prerun` mode and included in the generated `template.yaml`.
