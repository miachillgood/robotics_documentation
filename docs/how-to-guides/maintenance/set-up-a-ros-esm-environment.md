(how-to-guides-maintenance-set-up-a-ros-esm-environment)=

# Set up a ROS ESM environment

This guide will walk you through setting up
your environment once you've [enabled ROS ESM](enable-ros-esm.md).

You have a couple of different choices:
you can either install the complete ROS distro variant offered by ROS ESM (`ros_base`),
or you can use rosdep to install the specific dependencies required by your ROS project.
Let's quickly explore both options.

## Installing ROS ESM base variant

ROS ESM offers the upstream `metapackage` variant called `ros_base`,
which facilitates the installation of all ROS packages included in this variant.
For example,
if you are working with `Xenial` and its corresponding version ROS Kinetic,
run the command:

`````{tabs}

````{tab}  ROS Foxy

```bash
sudo apt install ros-foxy-ros-base
```
````

````{tab} ROS Noetic

```bash
sudo apt install ros-noetic-ros-base
```

````
````{tab} ROS Melodic

```bash
sudo apt install ros-melodic-ros-base
```

````
````{tab} ROS Kinetic

```bash
sudo apt install ros-kinetic-ros-base
```

````
`````

```{note}
Remember that the Ubuntu version and ROS version are co-dependent,
so you have to choose a pair. For example, Ubuntu 16.04 LTS and ROS Kinetic,
Ubuntu 18.04 LTS and ROS Melodic, Ubuntu 20.04 LTS and ROS Noetic/ROS 2 Foxy.
Here you can find more information for [ROS distributions](http://wiki.ros.org/Distributions)
and [ROS 2 distributions](https://docs.ros.org/en/foxy/Releases.html).
```

## Note on rosdep set up

Note that ROS ESM is its own ROS distribution,
and thus provides its own distribution and `rosdep` files.
If you already have upstream ROS installed and
initialised (e.g. you previously ran `sudo rosdep init`),
you’ll need to make sure you install `rosdep` from ESM and re-initialise it as follows:

```bash
sudo apt install python-rosdep
sudo rm /etc/ros/rosdep/sources.list.d/20-default.list
sudo rosdep init
rosdep update
```

## Installing ROS ESM project-specific dependencies

Typically, when using ROS ESM,
your ROS workspace would already be configured with the relevant source code.
In such cases,
it is highly recommended to accurately define the dependencies of
your packages in the *package.xml* file and
proceed by installing all the required ROS ESM dependencies
by executing the following command:

```bash
cd ros-ws
rosdep install --ignore-src --from-paths src
```

By doing so, the packages required for your project will be fetched and
installed from the `ROS ESM ppa`,
ensuring smooth operation.

## ESM and non-ESM components

A given ROS distribution includes a huge number of
packages with wildly varying levels of quality.
ROS ESM does not attempt to support them all,
and instead focuses on core functionality.

We of course realise that everyone’s needs are different, and are very open to
[receiving feedback](https://ubuntu.com/robotics/ros-esm#get-in-touch)
about anything that should be added to ROS ESM.
While such additions will need to pass some scrutiny,
we fully expect the number of ROS packages included in ESM to grow over time.

If you want to learn more about how to combine ROS ESM and upstream ROS components,
check out [this guide](combine-esm-and-upstream-ros.md).

To see which packages are currently being supported for each distro,
see [the current list of ROS packages included in ROS ESM](../../references/esm-package-list.md).
