# Running in Containers

This guide covers how to run Agnocast applications in Docker containers.

## Requirements

### Kernel module on the host

The Agnocast kernel module (`agnocast-kmod`) must be installed on the **host** system — it cannot run inside a container.

**Ubuntu hosts** — Install via apt as described in [Environment Setup](../environment-setup/index.md).

**Non-Ubuntu hosts** (or environments where `apt` is not available) — Build the kernel module from source:

```bash
git clone --branch 2.3.1 https://github.com/autowarefoundation/agnocast.git
cd agnocast/agnocast_kmod
make
sudo insmod agnocast.ko
```

!!! note
    Building from source requires kernel headers for your running kernel. The module supports kernel 5.x and 6.x series.

### Device access

Each container needs access to the Agnocast device file:

```bash
docker run --device /dev/agnocast ...
```

### Shared IPC namespace

Agnocast uses POSIX shared memory (`/dev/shm`) and POSIX message queues (`/dev/mqueue`) for inter-process communication. These resources are scoped by the Linux IPC namespace. By default, each Docker container gets its own private IPC namespace, meaning **Agnocast processes in different containers cannot communicate with each other**.

To enable communication, all Agnocast containers must share the same IPC namespace.

## IPC Namespace Configuration

### Option 1: Share the host IPC namespace

The simplest approach — all containers use the host's IPC namespace:

```bash
docker run --ipc=host --device /dev/agnocast ...
```

This also allows communication between containerized Agnocast processes and processes running directly on the host.

### Option 2: Share an IPC namespace between containers

If you don't want to expose the host IPC namespace, create a shared IPC namespace among containers:

**Start the first container with `--ipc=shareable`:**

```bash
docker run --ipc=shareable --device /dev/agnocast --name agnocast_main ...
```

**Start subsequent containers joining the first container's IPC namespace:**

```bash
docker run --ipc=container:agnocast_main --device /dev/agnocast ...
```

All containers sharing the same IPC namespace can communicate via Agnocast.

## Docker Compose Example

```yaml
services:
  node_a:
    image: my_ros2_image
    ipc: host
    devices:
      - /dev/agnocast

  node_b:
    image: my_ros2_image
    ipc: host
    devices:
      - /dev/agnocast
```

Or with a shared IPC namespace between containers only:

```yaml
services:
  node_a:
    image: my_ros2_image
    ipc: shareable
    devices:
      - /dev/agnocast

  node_b:
    image: my_ros2_image
    ipc: "service:node_a"
    devices:
      - /dev/agnocast
```
