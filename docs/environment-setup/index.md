# Environment Setup

## Prerequisites

- **ROS 2** Humble or Jazzy installed (rclcpp)
- **Ubuntu** 22.04 or 24.04
- **Linux kernel** 5.x or 6.x series

## Installation

Agnocast consists of three components:

| Component | Description | Installation |
|-----------|-------------|-------------|
| **agnocast-kmod** | Linux kernel module for core metadata management | apt (PPA) |
| **agnocast-heaphook** | Custom heap allocator for shared memory allocation | apt (PPA) |
| **ROS packages** (agnocastlib, etc.) | Core library and rclcpp-compatible pub/sub API | Source build |

The kernel module and heaphook are distributed via a Launchpad PPA with explicit version pinning.
The ROS packages are not yet available from the ROS build farm and must be built from source for now.

### 1. Add the Agnocast PPA

Import the GPG key and add the repository:

```bash
# Download and install the GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL 'https://keyserver.ubuntu.com/pks/lookup?op=get&search=0xCFDB1950382092423DF37D3E075CD8B5C91E5ACA' \
  | sudo gpg --dearmor -o /etc/apt/keyrings/agnocast-ppa.gpg

# Add the repository (DEB822 format)
sudo tee /etc/apt/sources.list.d/agnocast.sources > /dev/null <<EOF
Types: deb
URIs: http://ppa.launchpad.net/t4-system-software/agnocast/ubuntu
Suites: jammy
Components: main
Signed-By: /etc/apt/keyrings/agnocast-ppa.gpg
EOF

sudo apt update
```

### 2. Install the kernel module and heaphook

Install kernel headers (required for DKMS to build the kernel module) and the Agnocast packages:

```bash
sudo apt install linux-headers-$(uname -r)
sudo apt install \
  agnocast-kmod-v2.3.1 \
  agnocast-heaphook-v2.3.1
```

!!! note
    If you are running in a container environment, skip `agnocast-kmod` installation. The kernel module must be installed on the **host** system instead.

!!! note
    If `linux-headers-$(uname -r)` is not available (e.g., custom-built kernels), you must ensure the kernel headers matching your running kernel are installed manually before installing `agnocast-kmod`. DKMS requires them to compile the kernel module.

!!! note "Versioning rules"
    Agnocast follows semantic versioning (`major.minor.patch`):

    - **major** — Incremented when backward compatibility of the user-facing API is broken. The major version should not change within the same ROS 2 distribution (e.g., Humble or Jazzy).
    - **minor** — Incremented when the kmod syscall API changes. `agnocastlib` and `agnocast-kmod` with matching major and minor versions are guaranteed to work correctly together.
    - **patch** — Incremented for all other changes.

    Packages use version-pinned names (e.g., `agnocast-kmod-v2.3.1`) to ensure all components are at exactly the same version.

### 3. Build the ROS packages from source

Since the ROS packages are not yet distributed from the ROS build farm, build them from source:

```bash
git clone --branch 2.3.1 https://github.com/autowarefoundation/agnocast.git
cd agnocast
rosdep install --from-paths src --ignore-src -y
colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release
source install/setup.bash
```

!!! info
    Once the ROS build farm release is available, the ROS packages will also be installable via apt (e.g., `ros-jazzy-agnocast=2.3.1*`), and this source build step will no longer be necessary.

### 4. Load the kernel module

```bash
sudo modprobe agnocast
```

The kernel module accepts parameters to customize the shared memory pool:

```bash
sudo modprobe agnocast mempool_num=8192 mempool_size_gb=32
```

| Parameter | Description | Default |
|-----------|-------------|---------|
| `mempool_num` | Maximum number of memory pools (one per process) | 4096 |
| `mempool_size_gb` | Size of each memory pool in GB | 16 |
| `mempool_start_addr` | Virtual start address of the memory allocator | `0x40000000000` |

!!! note
    These parameters use virtual address space, not physical memory. Actual physical memory is allocated on demand as pages are touched.

To persist parameters and auto-load at boot:

```ini
# /etc/modprobe.d/agnocast.conf
options agnocast mempool_num=8192 mempool_size_gb=32
```

```bash
echo 'agnocast' | sudo tee /etc/modules-load.d/agnocast.conf
```

### 5. Verify installation

After building and sourcing the workspace, run the sample application:

```bash
# Terminal 1
source install/setup.bash
ros2 launch agnocast_sample_application talker.launch.xml

# Terminal 2
source install/setup.bash
ros2 launch agnocast_sample_application listener.launch.xml
```

## Next Steps

- [System Configuration](configuration.md) — required kernel parameters
- [Migration Guide](../migration-guide/index.md) — how to integrate Agnocast into your application
