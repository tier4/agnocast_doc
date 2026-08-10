# System Configuration

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
