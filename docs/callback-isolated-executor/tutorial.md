# Tutorial

This tutorial walks through the full workflow: launching a sample application with CallbackIsolatedExecutor, generating a thread configuration template, applying scheduling parameters, and verifying the result.

## Sample Application

The `cie_tutorial_node` in `agnocast_sample_application` is a simple node with three CallbackGroups, each running a timer at a different rate:

- **sensor_group** — 100 ms timer (high priority)
- **processing_group** — 200 ms timer (medium priority)
- **logging_group** — 1 s timer (low priority)

Each CallbackGroup gets a dedicated OS thread from the CallbackIsolatedExecutor.

## Step 1: Launch the application

```bash
ros2 launch agnocast_sample_application cie_tutorial.launch.xml
```

You should see interleaved log messages from the three callbacks.

## Step 2: Generate a template

Start the prerun node **before** launching your application:

```bash
ros2 run agnocast_cie_thread_configurator thread_configurator_node --prerun
```

Wait until the log output settles (all three CallbackGroups are discovered), then press Ctrl+C. A `template.yaml` is created in the current directory:

```yaml
hardware_info:
  model_name: ...
  ...

rt_throttling:
  runtime_us: 950000
  period_us: 1000000

callback_groups:
  - id: /cie_tutorial_node@Timer(100000000)
    affinity: ~
    policy: SCHED_OTHER
    priority: 0

  - id: /cie_tutorial_node@Timer(200000000)
    affinity: ~
    policy: SCHED_OTHER
    priority: 0

  - id: /cie_tutorial_node@Timer(1000000000)
    affinity: ~
    policy: SCHED_OTHER
    priority: 0

non_ros_threads: []
```

Stop the sample application (Ctrl+C).

## Step 3: Edit the configuration

Copy and edit the template to assign real-time priorities:

```bash
cp template.yaml cie_tutorial_config.yaml
```

Example configuration:

```yaml
rt_throttling:
  runtime_us: 950000
  period_us: 1000000

callback_groups:
  - id: /cie_tutorial_node@Timer(100000000)
    policy: SCHED_FIFO
    priority: 90
    affinity: [0]

  - id: /cie_tutorial_node@Timer(200000000)
    policy: SCHED_FIFO
    priority: 80
    affinity: [1]

  - id: /cie_tutorial_node@Timer(1000000000)
    policy: SCHED_OTHER
    priority: 0

non_ros_threads: []
```

This gives the sensor timer the highest real-time priority on CPU 0, the processing timer a lower real-time priority on CPU 1, and leaves the logging timer on the default CFS scheduler.

## Step 4: Launch with configuration

Before the first run, complete the [thread configurator setup](integration-guide.md#step-2-set-up-the-thread-configurator) (grant capabilities and configure library paths).

Then start the configurator:

```bash
ros2 run agnocast_cie_thread_configurator thread_configurator_node --config-file cie_tutorial_config.yaml
```

Then, in another terminal, launch the application:

```bash
ros2 launch agnocast_sample_application cie_tutorial.launch.xml
```

The configurator will log messages as it applies the configuration to each discovered CallbackGroup.

## Step 5: Verify

While the application is running, verify the thread scheduling with `chrt` and `taskset`:

```bash
# Find the thread IDs
ps -eLo pid,tid,cls,rtprio,psr,comm | grep cie_tutorial

# Example output (several threads, including internal ones):
#    PID    TID CLS RTPRIO PSR COMMAND
# 429255 429255  TS      -   9 cie_tutorial_no
# 429255 429257  TS      -   8 cie_tutorial_no
# 429255 429265  TS      -   0 cie_tutorial_no
# 429255 429266  TS      -   5 cie_tutorial_no
# 429255 429267  FF     90   0 cie_tutorial_no  <-- sensor timer
# 429255 429268  FF     80   1 cie_tutorial_no  <-- processing timer
# 429255 429269  TS      -  15 cie_tutorial_no  <-- logging timer (CFS)
```

- `FF` = SCHED_FIFO, `TS` = SCHED_OTHER (CFS)
- `rtprio` shows the real-time priority
- `psr` shows the CPU the thread last ran on
- Threads without RTPRIO are internal threads (default callback group, bridge daemon, etc.)

You can also verify individual threads:

```bash
chrt -p <tid>    # Show scheduling policy and priority
taskset -p <tid> # Show CPU affinity mask
```

See the [YAML Specification](yaml-specification.md) for all available configuration options.
