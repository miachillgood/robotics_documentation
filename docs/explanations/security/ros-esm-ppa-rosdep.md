# Interaction between ROS ESM and ROS upstream

When enabling ROS ESM using `pro enable ros` as described in
{ref}`this guide <how-to-guides-maintenance-enable-ros-esm>`,
some changes are made to `apt` configuration and it's important to be aware
of those details.

## Changes to `PPAs`

If you followed the official installation instructions for
[ROS 1](https://wiki.ros.org/noetic/Installation/Ubuntu)
or [ROS 2](https://docs.ros.org/en/rolling/Installation/Ubuntu-Install-Debs.html),
you now have some additional files in your `/etc/apt/sources.list.d` folder.

These files are telling your apt software which server is able to provide specific packages.
For the ROS ecosystem the files are usually called:

- `/etc/apt/sources.list.d/ros-latest.list` for ROS 1
- `/etc/apt/sources.list.d/ros2.list` for ROS 2

For example, when you request `apt` to install `ros-noetic-std-msgs`,
it will fetch it from the server written inside the `ros-latest.list` file.
When you enable ROS ESM,
you will notice that a new configuration file is added inside your `sources.list.d` folder.
The file is called `ubuntu-ros.list` and tells `apt` to fetch packages from [esm.ubuntu.com](https://esm.ubuntu.com).
Our ESM packages can be distinguished because their version follows the pattern
`X.Y.Z+<ubuntu-version>-<counter>` where:

- `X.Y.Z` is the usual ROS versioning system
- `<ubuntu-version>` is an LTS name such as `20.04.1`
- `<counter>` is a single integer.

After enabling ROS ESM you can inspect a package with `apt-cache`.
For example:

```bash
apt-cache policy ros-foxy-std-msgs
```

```bash
ros-foxy-std-msgs:
  Installed: 2.0.5-1focal.20230527.044919
  Candidate: 2.0.5+20.04.1-0
  Version table:
     2.0.5+20.04.1-0 500
        500 https://esm.ubuntu.com/ros/ubuntu focal-security/main amd64 Packages
 *** 2.0.5-1focal.20230527.044919 500
        500 http://packages.ros.org/ros2/ubuntu focal/main amd64 Packages
        500 http://repo.ros2.org/ubuntu/main focal/main amd64 Packages
        100 /var/lib/dpkg/status
```

This indicates that `ros-foxy-std-msgs` is available on ros.org at version `2.0.5-1focal`,
while the ROS ESM repository provides version `2.0.5+20.04.1-0`.

Apt automatically decides to upgrade from upstream `ros.org` to ROS ESM if both are available,
you can confirm this by running:

```bash
$ apt list --upgradable
ros-foxy-std-msgs/focal-security 2.0.5+20.04.1-0 amd64 [upgradable from: 2.0.5-1focal.20230527.044919]
```

If you want to be sure you no longer consume any End-of-Life upstream packages,
you should remove the `ros-latest.list` and `ros2.list` files and update your apt cache.

```bash
sudo rm /etc/apt/ros-latest.list /etc/apt/ros2.list
sudo apt update
```

## Changes to rosdep

ROS ESM is its own ROS distribution,
and thus provides its own distribution and `rosdep` files.
If you already have upstream ROS installed and initialised
(e.g. you previously ran `sudo rosdep init`),
you’ll need to make sure you install `rosdep` from ESM and
re-initialise it as follows:

`````{tabs}

````{tab}  Noetic/Foxy (Python3)

```bash
sudo apt install python3-rosdep
sudo rm /etc/ros/rosdep/sources.list.d/20-default.list
sudo rosdep init
rosdep update
```
````

````{tab} Kinetic/Melodic (Python2)

```bash
sudo apt install python-rosdep
sudo rm /etc/ros/rosdep/sources.list.d/20-default.list
sudo rosdep init
rosdep update
```

````
`````

Now, the output of running `rosdep update` will look like the following:

```bash
$ rosdep update
reading in sources list data from /etc/ros/rosdep/sources.list.d
Hit https://ros.robotics.ubuntu.com/rosdep/osx-homebrew.yaml
Hit https://ros.robotics.ubuntu.com/rosdep/base.yaml
Hit https://ros.robotics.ubuntu.com/rosdep/python.yaml
Hit https://ros.robotics.ubuntu.com/rosdep/ruby.yaml
Hit https://ros.robotics.ubuntu.com/rosdep/fuerte.yaml
Query rosdistro index https://staging.ros.robotics.ubuntu.com/rosdistros/index-v4.yaml
Add distro "foxy"
Add distro "kinetic"
Add distro "melodic"
Add distro "noetic"
updated cache in /home/user/.ros/rosdep/sources.cache
```
