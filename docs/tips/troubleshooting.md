# Troubleshooting

## Cleaning up shared memory and message queues

Agnocast runs a daemon process that automatically cleans up shared memory and message queues, even when Agnocast participant processes crash. If the daemon itself is killed, these resources may persist. Clean them up manually:

```bash
# Shared memory
rm /dev/shm/agnocast@*

# Message queues
rm /dev/mqueue/agnocast@*
rm /dev/mqueue/agnocast_bridge_manager@*
```
