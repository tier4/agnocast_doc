# Running in Containers

This guide covers how to run Agnocast applications in Docker containers.

## Requirements

### Kernel module on the host

The Agnocast kernel module (`agnocast-kmod`) must be installed on the **host** system — it cannot run inside a container.

**Ubuntu hosts** — Install via apt as described in [Environment Setup](../environment-setup/index.md).

**Non-Ubuntu hosts** (or environments where `apt` is not available) — Build the kernel module from source:

```bash
git clone --branch 2.3.3 https://github.com/autowarefoundation/agnocast.git
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

## Swapping the host kernel module

When you need to change the host's `agnocast-kmod` version independently of the heaphook bundled in the container (for example, after rolling the container image to a new version, or to reproduce a bug on an older kmod), use [`switch_kmod.bash`](https://github.com/autowarefoundation/agnocast/blob/main/scripts/switch_kmod.bash):

```bash
sudo ./scripts/switch_kmod.bash <VERSION>
# e.g.
sudo ./scripts/switch_kmod.bash 2.4.0
```

The script unloads the current module, purges every installed `agnocast-kmod-v*` package, cleans any leftover DKMS state, installs the target from apt, and verifies the new load via `dmesg`.

!!! warning
    All Agnocast containers and ROS nodes must be stopped before running this script — the module cannot be unloaded while `/dev/agnocast` is held open.

!!! warning
    The kmod version on the host and the `libagnocast_heaphook.so` version inside the container must share the same ioctl ABI. Mismatched versions cause runtime errors. This script does not touch the container; it is the operator's responsibility to roll the container to a matching version.

After the swap, verify that the host kmod, the in-container `libagnocast_heaphook.so`, and the in-container `agnocastlib` are on compatible versions by running

```bash
source <your-workspace>/install/setup.bash   # must include the ros2agnocast package
ros2 agnocast -v
```

**inside the container** where your Agnocast application actually runs. The command prints the detected kmod / heaphook / agnocastlib versions and flags any incompatibility.
