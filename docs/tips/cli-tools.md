# CLI Tools

Agnocast extends the `ros2` command line with additional commands for inspecting Agnocast topics and nodes.

## Topic Commands

### List Agnocast Topics

```bash
ros2 topic list_agnocast
```

Lists all active Agnocast topics with their message types.

**Verbose mode** (`-v`):

```bash
ros2 topic list_agnocast -v
```

Shows additional details including publisher and subscriber counts.

### Inspect a Topic

```bash
ros2 topic info_agnocast /my_topic
```

Shows publishers and subscribers for an Agnocast topic.

**Verbose mode** (`-v`):

```bash
ros2 topic info_agnocast /my_topic -v
```

Shows detailed information including process IDs, entry statuses, and subscriber statuses.

**Debug mode** (`-d`):

```bash
ros2 topic info_agnocast /my_topic -d
```

Shows internal debug information including shared memory details.

## Node Commands

### List Agnocast Nodes

```bash
ros2 node list_agnocast
```

Lists all active Agnocast nodes.

### Inspect a Node

```bash
ros2 node info_agnocast /my_node
```

Shows publishers and subscribers for an Agnocast node, grouped by topic.

## Publisher/Subscriber Status

The `info_agnocast` command shows the status of each publisher entry and subscriber:

### Publisher Entry Status

| Status | Meaning |
|--------|---------|
| `RC > 0` | Entry is currently referenced by subscribers |
| `RC = 0` | Entry has no active references |
| `RELEASED` | Entry has been released by the publisher |

### Subscriber Status

| Status | Meaning |
|--------|---------|
| `ACTIVE` | Subscriber is actively receiving messages |
| `WAITING` | Subscriber is waiting for new messages |
