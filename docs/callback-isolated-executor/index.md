# CallbackIsolatedExecutor

The `CallbackIsolatedAgnocastExecutor` assigns a dedicated OS thread to each CallbackGroup, enabling per-callback scheduling control (policy, priority, CPU affinity). It is the Agnocast-compatible version of [callback_isolated_executor](https://github.com/autowarefoundation/callback_isolated_executor).

## Why

Standard ROS 2 executors share threads across callbacks — you cannot control which callback runs on which CPU or at what priority.

```
Standard Executor:                  CallbackIsolatedExecutor:

  CallbackGroup A ─┐                 CallbackGroup A → Thread (FIFO, prio=90, CPU0)
  CallbackGroup B ─┼→ Thread Pool    CallbackGroup B → Thread (FIFO, prio=80, CPU1)
  CallbackGroup C ─┘                 CallbackGroup C → Thread (CFS, nice=0)

  No per-callback control            Full OS-level scheduling control
```

With CallbackIsolatedExecutor, each CallbackGroup maps to exactly one OS thread. Scheduling is handled entirely by the Linux kernel — you directly assign SCHED_FIFO, SCHED_RR, SCHED_DEADLINE, or CFS parameters per callback.

For the design rationale and evaluation, see the RTAS 2025 paper: [*Middleware-Transparent Callback Enforcement in Commoditized Component-Oriented Real-time Systems*](https://arxiv.org/pdf/2505.06546).

!!! note
    `CallbackIsolatedAgnocastExecutor` does not require `agnocast-kmod` or `agnocast-heaphook`. If you only want per-callback scheduling control without Agnocast's zero-copy IPC, you can use the executor on its own — just install the `agnocastlib` ROS package.

## Naming

| | Original | Agnocast Version |
|--|----------|------------------|
| Package | `callback_isolated_executor` | `agnocast_components` or `agnocastlib` |
| Executor Class | `CallbackIsolatedExecutor` | `agnocast::CallbackIsolatedAgnocastExecutor` |
| Container Executable | `component_container_callback_isolated` | `agnocast_component_container_cie` |
| Thread Configurator | `cie_thread_configurator` | `agnocast_cie_thread_configurator` |

## Executor Variants

| Executor | Handles ROS 2 Callbacks | Handles Agnocast Callbacks | Use Case |
|----------|------------------------|---------------------------|----------|
| `CallbackIsolatedAgnocastExecutor` | Yes | Yes | Stage 1 or mixed Stage 1/2 |
| `AgnocastOnlyCallbackIsolatedExecutor` | No | Yes | Stage 2 only |

## Pages

- [Integration Guide](integration-guide.md) — How to introduce CallbackIsolatedExecutor and set up the thread configurator
- [YAML Specification](yaml-specification.md) — Complete reference for the thread configuration file
- [Non-ROS Threads](non-ros-threads.md) — Managing scheduling for threads outside the ROS 2 executor
- [Tutorial](tutorial.md) — End-to-end walkthrough with a sample application
