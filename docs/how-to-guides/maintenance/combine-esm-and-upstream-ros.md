(how-to-guides-maintenance-combine-esm-and-upstream-ros)=

# Combine ESM and upstream ROS components

We don't support enabling both ROS ESM as well as the upstream ROS Debian repository.
This means that every ROS component you use must either be from ESM,
or built from source against ESM.

There is tooling that makes this fairly straightforward, called `rosinstall_generator`,
that will generate a rosinstall file containing the desired package(s) and
all dependencies not already satisfied.

In a sourced ROS ESM environment, execute the following:

`````{tabs}
````{tab} Noetic/Melodic

```bash
sudo apt install python-rosinstall-generator
export ROSDISTRO_INDEX_URL="https://raw.githubusercontent.com/ros/rosdistro/master/index-v4.yaml"
rosinstall_generator <package>  --rosdistro <ros-distro>  --deps-up-to RPP > ~/extra-stuff.rosinstall
```

For example:

```bash
rosinstall_generator desktop_full --rosdistro noetic --deps-up-to RPP > ~/extra-stuff.rosinstall
```

Once that file is obtained, there are a few steps left to have the software usable.

First, if there isn’t a workspace already, this needs to be created:

``` bash
mkdir -p ~/ros_ws/src
```

If not already installed, install `vcs-tool` with the following command:

```bash
curl -s https://packagecloud.io/install/repositories/dirk-thomas/vcstool/script.deb.sh | sudo bash
sudo apt-get update
sudo apt-get install python3-vcstool
```

Then the repos in the rosinstall file need to be fetched into
the workspace with the following command:

```bash
cd ~/ros_ws
vcs import --shallow < ~/extra-stuff.rosinstall
```

Now dependencies of the workspace need to be installed:

```bash
cd ~/ros_ws
rosdep install --ignore-src --from-paths src --default-yes
```

Finally, the workspace needs to be built:

```bash
cd ~/ros_ws
catkin_make_isolated
```
````

````{tab} Foxy

```bash
sudo apt install python3-rosinstall-generator
export ROSDISTRO_INDEX_URL="https://raw.githubusercontent.com/ros/rosdistro/master/index-v4.yaml"
rosinstall_generator <package>  --rosdistro <ros-distro>  --deps-up-to RPP > ~/extra-stuff.rosinstall
```

For example:

```bash
rosinstall_generator desktop_full --rosdistro foxy --deps-up-to RPP > ~/extra-stuff.rosinstall
```

Once that file is obtained, there are a few steps left to have the software usable.

First, if there isn’t a workspace already, this needs to be created:

``` bash
mkdir -p ~/ros_ws/src
```

If not already installed, install `vcs-tool` with the following command:

```bash
curl -s https://packagecloud.io/install/repositories/dirk-thomas/vcstool/script.deb.sh | sudo bash
sudo apt-get update
sudo apt-get install python3-vcstool
```

Then the repos in the rosinstall file need to be fetched into
the workspace with the following command:

``` bash
cd ~/ros_ws
vcs import --shallow < ~/extra-stuff.rosinstall
```

Now dependencies of the workspace need to be installed:

```bash
cd ~/ros_ws
rosdep install --ignore-src --from-paths src --default-yes
```

Finally, the workspace needs to be built:

``` bash
cd ~/ros_ws
colcon build --cmake-args -DCMAKE_BUILD_TYPE=Release
```
````

````{tab} Kinetic

```bash
sudo apt install python-rosinstall-generator
export ROSDISTRO_INDEX_URL="https://raw.githubusercontent.com/ros/rosdistro/master/index-v4.yaml"
rosinstall_generator <package>  --rosdistro <ros-distro>  --deps-up-to RPP > ~/extra-stuff.rosinstall
```

For example:

```bash
rosinstall_generator desktop_full --rosdistro kinetic --deps-up-to RPP > ~/extra-stuff.rosinstall
```

Once that file is obtained, there are a few steps left to have the software usable.

First, if there isn’t a workspace already, this needs to be created:

``` bash
mkdir -p ~/ros_ws/src
```

If not already installed, install `wstool` with the following command:

```bash
sudo apt-get install python-wstool
```

Then the repos in the rosinstall file need to be fetched into
the workspace with the following command:

``` bash
cd ~/ros_ws
wstool init src ~/extra-stuff.rosinstall
```

Now dependencies of the workspace need to be installed:

```bash
cd ~/ros_ws
rosdep install --ignore-src --from-paths src --default-yes
```

Finally, the workspace needs to be built:

``` bash
cd ~/ros_ws
catkin_make_isolated
```
````
`````

That builds the required software against the ESM ROS release, where ABI will not break.
Once the process is complete, the required software is available in the workspace.

```{important}
Since ROS Groovy,
not all packages belonging to the `desktop_full` `metapackage` have been `catkinized`.
As a result, when using `rosinstall_generator`,
it is necessary to compile the workspace using `catkin_make_isolated`.
```
