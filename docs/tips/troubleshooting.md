# Troubleshooting

## Cleaning up shared memory

Agnocast runs a daemon process that automatically cleans up shared memory, even when Agnocast participant processes crash. If the daemon itself is killed, these resources may persist. Clean them up manually:

```bash
rm /dev/shm/agnocast@*
```
