# Upgrading Agnocast

This page describes how to upgrade Agnocast to a new version. All three components — agnocast-kmod, agnocast-heaphook, and the ROS packages — must be upgraded together to the same version.

## 1. Install the new version of the kernel module and heaphook

Installing the new kmod package automatically removes the old DKMS registration:

```bash
sudo apt install \
  agnocast-kmod-v<NEW_VERSION> \
  agnocast-heaphook-v<NEW_VERSION>
```

For example, to upgrade from 2.3.1 to 2.4.0:

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
    Once the ROS build farm release is available, the ROS packages will also be installable via apt (e.g., `ros-jazzy-agnocast=2.3.1*`), and this source build step will no longer be necessary.

## 3. Reload the kernel module

```bash
sudo modprobe -r agnocast
sudo modprobe agnocast
```

!!! warning
    All Agnocast processes must be stopped before reloading the kernel module.

## Version compatibility

When upgrading, keep the [versioning rules](index.md) in mind:

- **Patch upgrades** (e.g., 2.3.1 → 2.3.2) — Safe. No API or syscall changes.
- **Minor upgrades** (e.g., 2.3.x → 2.4.0) — `agnocastlib` and `agnocast-kmod` must be upgraded together, as the kmod syscall API may have changed.
- **Major upgrades** — User-facing API may have breaking changes. Review the changelog before upgrading.
