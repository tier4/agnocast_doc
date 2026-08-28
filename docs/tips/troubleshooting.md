# Troubleshooting

## Cleaning up shared memory and message queues

Agnocast runs a daemon process that automatically cleans up shared memory and message queues, even when Agnocast participant processes crash. If the daemon itself is killed, these resources persist until the next Agnocast process starts, which spawns a replacement that unlinks them. To clean them up without waiting for that:

```bash
# Shared memory
rm /dev/shm/agnocast@*

# Message queues
rm /dev/mqueue/agnocast@*
rm /dev/mqueue/agnocast_bridge_manager@*
```
