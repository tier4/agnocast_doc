# Upgrading Agnocast

This page describes how to upgrade Agnocast to a new version. All three components — agnocast-kmod, agnocast-heaphook, and the ROS packages — must be upgraded together to the same version.

## 1. Install the new version of the kernel module and heaphook

Installing the new kmod package automatically removes the old DKMS registration:

```bash
sudo apt install \
  agnocast-kmod-v<NEW_VERSION> \
  agnocast-heaphook-v<NEW_VERSION>
```

For example, to upgrade from 2.3.3 to 2.4.0:

```bash
sudo apt install agnocast-kmod-v2.4.0 agnocast-heaphook-v2.4.0
```

## 2. Rebuild the ROS packages from source

```bash
cd agnocast
git fetch
git checkout <NEW_VERSION>
colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release
source install/setup.bash
```

!!! info
    Once the ROS build farm release is available, the ROS packages will also be installable via apt (e.g., `ros-jazzy-agnocast=2.3.3*`), and this source build step will no longer be necessary.

## 3. Reload the kernel module

```bash
sudo modprobe -r agnocast
sudo modprobe agnocast
```

!!! warning
    All Agnocast processes must be stopped before reloading the kernel module.

## Version compatibility

When upgrading, keep the [versioning rules](index.md) in mind:

- **Patch upgrades** (e.g., 2.3.3 → 2.3.2) — Safe. No API or syscall changes.
- **Minor upgrades** (e.g., 2.3.x → 2.4.0) — `agnocastlib` and `agnocast-kmod` must be upgraded together, as the kmod syscall API may have changed.
- **Major upgrades** — User-facing API may have breaking changes. Review the changelog before upgrading.

## Switching only the host kmod (container-based setups)

When Agnocast workloads run inside a container, `agnocast-heaphook` is bundled with the container image and is swapped by rolling to a new container. In that setup, only the host-side `agnocast-kmod` needs to be replaced independently to keep the ioctl ABI in sync with the heaphook inside the container.

The [`switch_kmod.bash`](https://github.com/autowarefoundation/agnocast/blob/main/scripts/switch_kmod.bash) script automates the host-side kmod swap:

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
