# System Configuration

## Kernel Parameters

Agnocast uses POSIX message queues for inter-process notification. The default Linux limits are too low for typical robotics workloads.

### Required

Set the maximum number of messages per queue:

```bash
sudo sysctl -w fs.mqueue.msg_max=256
```

To persist across reboots, add to `/etc/sysctl.d/agnocast.conf`:

```ini
fs.mqueue.msg_max = 256
```

### Optional (for large deployments)

```ini
# Maximum number of message queues system-wide
fs.mqueue.queues_max = 1024
```

If running many Agnocast processes, you may also need to increase the per-user message queue memory limit:

```bash
# In /etc/security/limits.conf or systemd unit
* - msgqueue unlimited
```

## RT Throttling (for CallbackIsolatedExecutor)

If using real-time scheduling with the CallbackIsolatedExecutor, you may need to increase the RT throttling limit. The default allows RT tasks to use 95% of each period:

```ini
# /etc/sysctl.d/agnocast-rt.conf
kernel.sched_rt_period_us = 1000000
kernel.sched_rt_runtime_us = 980000
```

This allows RT tasks to use up to 98% of each 1-second period, leaving 20 ms for non-RT tasks.

!!! warning
    Setting `sched_rt_runtime_us = -1` disables RT throttling entirely, which can lock up the system if an RT task runs away. Only use `-1` if you fully understand the implications.

