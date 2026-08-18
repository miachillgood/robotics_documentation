(tutorials-snaps-core-packaging-complex-robotics-software-with-snaps)=

# Packaging complex robotics software with snaps

```{important}

 **Before you start**

1. Make sure you have completed {ref}`Tutorial 1: Packaging our first ROS application as a snap <tutorials-snaps-core-packaging-ros-application-getting-started>`
before starting this tutorial.
This tutorial builds on key concepts introduced earlier,
including the benefits of snaps for ROS applications and
the essential features of Snapcraft.

2. This guide is meant for ROS snap beginners and
advanced users looking for guidelines.

3. This is not a quick guide  nor a ROS tutorial.
A new developer will take approximately **one full day** to cover the entire guide.
```

The first step for deploying a robotics application is to package it.
Snaps are specifically designed to confine embedded Linux applications,
making it easier to install and manage software versions.
They offer useful features for deployment, such as over-the-air (OTA) updates,
delta updates, automatic rollback, security policies, and more.
While bundling all software dependencies,
snaps provide a comprehensive deployment infrastructure for robotics software.

While snaps adapt to the way ROS developers work,
they bring new concepts and tools that we need to understand first.

## How to use this developer guide

In {ref}`Tutorial 1: Packaging our first ROS application as a snap <tutorials-snaps-core-packaging-ros-application-getting-started>`
of our developer guide series,
we introduced the main concepts and learned what snaps can do for ROS applications.
We also explored the most important features of Snapcraft.

In this developer guide,
we will explore advanced snap topics and tools that will show you how to structure,
package, and test complex robotics applications.

While this developer guide is meant to be read completely,
a second-time reader or an experienced snapcraft developer
might come back to a specific section.
Some sections can be used independently to learn how to solve a specific problem.

## What we will learn

Deploying robotics software is usually tackled when a project reaches certain maturity.
We need a fast and reliable way to distribute software and subsequent updates.
Additionally, we need the deployed software to be fully isolated in its sandbox,
thus minimizing security risks.

Addressing those points and more,
snaps represent an ideal solution to deploy ROS applications to devices and users.

Snapping a simple talker-listener in
{ref}`Tutorial 1: Packaging our first ROS application as a snap <tutorials-snaps-core-packaging-ros-application-getting-started>`
was good enough to see the potential of snaps.
However, when packaging a more complex application, one might wonder:

- Should we build one snap for our entire robot?
- Should we have one part per ROS package?
- What should a final robot snap look like?

Snap and snapcraft contain tons of features that will come in handy when
defining our robot application.
This guide will help you understand these features and how to use them.

In this second part, we will learn:

- How to create a snap for a robot software stack.
- How to take the decisions that a ROS snap developer has to take to design a snap.
- We will introduce new features and
  concepts associated with snaps that will be useful in a robot application.
- The different means to debug a snap package and its snapped applications.

While covering the theoretical aspects of ROS snaps,
we will apply all this knowledge to [TurtleBot3](https://emanual.robotis.com/docs/en/platform/turtlebot3/overview/)
for a more interesting real-world scenario.

## Requirements

1. You will need basic ROS knowledge.
  Ideally, you will already understand how to build packages, call a service,
  and know what a launch file is.
  You should also be familiar with the process of creating a map and
  using it to navigate.
2. A basic understanding of the Linux environment (Ubuntu) is also required.
3. You should have a working knowledge of snaps.
  This means either previous experience with snap and snapcraft,
  or having followed the
  {ref}`tutorials-snaps-core-packaging-ros-application-getting-started`.

### Setup

Since this developer guide builds a snap for a robot, we will need:

- TurtleBot3 [Gazebo classic](https://classic.gazebosim.org/)
  simulation running under ROS Noetic.
- Depending on our current OS,
  we can choose between the following Native setup and the Multipass setup.

`````{tabs}
````{group-tab} Option 1: Native Setup

The Native setup will need [Ubuntu 20.04](https://releases.ubuntu.com/focal/).
This is because we will need the TurtleBot3 simulation to run.
We don’t intend to embed the simulation into our snap.

With the running Ubuntu 20.04, follow the next step to install all the dependencies:

- Install ROS Noetic desktop-full following the [official documentation](http://wiki.ros.org/noetic/Installation/Ubuntu)
- Install the TurtleBot3 simulation with the following command:

  ```bash
  sudo apt install -y ros-noetic-turtlebot3-gazebo
  ```

- Make sure [snapd](https://snapcraft.io/docs/tutorials/install-the-daemon/) and
  [snapcraft](https://snapcraft.io/snapcraft) are installed

````

````{group-tab} Option 2: Multipass

  If a native setup is not possible, we will use a Virtual Machine.
  In this case, we are going to use [Multipass](https://documentation.ubuntu.com/multipass/stable/)
  to quickly generate an Ubuntu VM.

  ##### Install Multipass

  - On Ubuntu, the installation of Multipass is straightforward:

    ```bash
    sudo snap install multipass
    ```

  - We can also install it on Windows and macOS by following the [documentation](https://documentation.ubuntu.com/multipass/stable/).

  ##### Launch the VM

  - To launch the VM, we are going to use a [cloud-init](https://canonical-cloud-init.readthedocs-hosted.com/en/latest/)
    configuration stored in GitHub.
    In essence, we will launch the VM,
    and install ROS Noetic along with the TurtleBot3 simulation automatically.
    Note that this might take some time depending on our configuration (~15 minutes).

    ```bash
    multipass launch --cpus 2 --disk 20G --memory 4G --cloud-init https://raw.githubusercontent.com/canonical/ros_snap_workshop_part2_multipass/main/cloud-init.yaml 20.04 --name workshop-part2 --timeout 10000
    ```

  - The VM must now be up and running. We can verify that with:

    ```bash
    $ multipass list

    Name           State   IPv4       Image

    workshop-part2 Running 10.26.1.87 Ubuntu 20.04 LTS
    ```

  ##### Attach to the VM

  - Multipass offers a way to attach a shell to the VM with:

    ```bash
    multipass shell workshop-part2
    ```

  - Unfortunately, with this solution,
    we cannot forward X11 (for graphic applications).

  - We can connect with ssh into the VM with X11 forwarding with the command:

    ```bash
    ssh -X ubuntu@$(multipass list --format csv | awk -F, '$1=="workshop-part2"{print $3}')
    ```
  - The password for the Ubuntu user is simply: Ubuntu.

    ```{caution}
    Using a VM with a pre-saved password is not a good practice in general.
    Here we only do so to make it simple to follow the developer guide.
    If you wish to use a VM for anything else please change the password.*
    ```

  - In the case of a VM setup,
    all the commands and instructions from this guide must be executed in the VM.

````
`````

### Setup Check

We can make sure that everything is properly installed by launching:

```bash
TURTLEBOT3_MODEL=waffle_pi roslaunch turtlebot3_gazebo turtlebot3_world.launch
```

We should then see the TurtleBot3 simulated in the `turtlebot3_world` environment:

![|624x401](https://lh6.googleusercontent.com/5gAV3AtN7ZwfGeY-wtfQl6qRjoCBh9J16udACglEBT83gVGSWTVj30afDCF0NpGKIbA2G9Ygz-SOtn2c8JiIyedoh8CdtMNGYS9WB5PxD7pC7D9U3nDdnIzZ_Y1sDhTF7sSotFa7mYTofCUCQkUakw)

We can now `ctrl-c` the Gazebo launch file.

We can also:

```{warning}
Make sure to check your snapcraft version.
This tutorial is using Noetic which require an older version of snapcraft (8.x/stable).
```

```bash
snapcraft --version
```

And it should display a version below `9.0.0`.

You can always refresh snapcraft to the correct version with:

```
sudo snap refresh snapcraft --channel=8.x/stable
```

We are now all set up for this developer guide.

(identification-of-robot-components)=

## Identification of robot components

While we can find many examples to snap various applications,
robots might sound more complicated.
A robot is usually composed of multiple applications, background services,
and applications to call.

Snaps are designed to deploy applications.
Thus, **we must think of our robot software as an application and**
**not as a set of launch files**
to call in 5 different terminals.

To start snapping our stack we first need to
[identify the various functionalities and applications of our robot application](https://ubuntu.com/robotics/docs/identify-functionalities-and-applications-of-a-robotics-snap).

We are going to apply the methodology to the TurtleBot3.
This way, we will have a clear example of the functionalities and snap
entries for a robot,
as well as the process to identify these entries.

For this guide,
we will focus on the monolithic snap approach since
it is the simplest for a first robot snap.
All the possible architectures for ROS snap applications are described
{ref}`in the documentation <explanations-snaps-ros-architectures-with-snaps>`.

### Functionalities of our robot snap

Before defining our applications,
we must define the final functionalities that the snap should bring to our robot.
We want the user to do three things:

1. Teleoperate the robot with a keyboard or a joystick.
2. Create a map of our environment.
3. Navigate into our mapped environment.

These are the three functionalities that we want our users
to be able to perform with our robot.

Additionally, we don’t want our snap to be compatible only with our physical TurtleBot3.
We also want our snap to be compatible with the simulation.

Note that **we won’t need the snap to run the simulation itself**,
since the simulation is a substitute for the real robot.
**The snap should simply interface with the simulation.**

### Defining the TurtleBot3 applications

Now that we have defined the functionalities of the robot,
let’s have a look at the applications we need to cover them.

We want most of it to be ready as quickly as possible on the robot.
Hence, the common set of nodes for these functionalities must be always up and running.
We will call it the **core** application.

The diagram below summarises all these different applications inside our
TurtleBot3c (C for Canonical) snap and how they will be used by the final user.
The TurtleBot3C snap contains all the system and ROS dependencies for our applications.
We have `core` and `teleop` which are daemons started automatically at boot since
they are always necessary.
`Joy` and `key` apps are applications that can be called from the terminal by
a user to be able to control the robot manually.
Finally, `mapping` and `navigation` are background applications that can be
enabled or disabled.
Once enabled they will act exactly like `core` and
simply automatically start at boot.
All these applications are communicating with each other with ROS.

<https://assets.ubuntu.com/v1/2529db37-tb3snap.png>

Let’s break down what each of these applications will do and the requirements they have.

#### Core

Core is going to be our common set of nodes always running in the background.
In the case of the TurtleBot3,
we are talking about all the nodes to interface with the hardware
(mobile base, LIDAR, camera)
as well as the `robot_state_publisher` to have the model of the robot available.
This `core` snap application must be running in the background.

#### Teleoperation applications

TurtleBot3 should have the functionality to be
teleoperated with a joystick or a keyboard.
We want to be able to do that from a controller connected to the robot.
We also want another computer on the network to be able to control our robot.

To be able to manage so many different ways of teleoperating the robot,
we will need an application to be able to route all this traffic.
Similarly to the core app enabling the common part of all functionalities,
the `teleop` app will be starting the common part necessary
for all teleoperation scenarios.

On the contrary,
we don’t want the joystick or keyboard specific apps to be running all the time.

We will then need three different snap applications:

- The first one called `teleop` simply runs the teleoperation basics in the background.
  This way, a controller application running on the robot or
  remotely can always control the robot.
- The second application will be called `joy` and
  will be a command to call whenever we want to control the robot with a joystick.
  Meaning that every node and
  configuration specific to the joystick control should be launched in the application.
- The third application, `key`, will be similar to the `joy` application,
  but for the keyboard control.

You can see all of them in the diagram above.
This is an example of how we can split our applications.
Depending on the use case one might decide for a different split.

With these three different snap applications,
we will be able to have all the teleoperation functionality that we wanted.

#### Mapping

We will use TurtleBot3 to create a map of its environment.
Thus, we want a `mapping` application that we can call to start mapping our environment.
We also want this application to automatically save the map when we stop the application.
This way there will be no need to manipulate any file or to call a service of any kind.

Remember that the idea is to think of creating an application for deployment.
The final user of our snap will understand what creating a map of the environment means.
On the contrary, our end-user might not know ROS and thus how to save a map the ROS way
(calling a `rosservice` from the `map_server`).

Since the `core` & `teleop` daemons will be running,
launching `joy` or `key` along with `mapping` will be all we need to start
creating a map of any environment.

#### Navigation

After mapping, we navigate in our freshly mapped environment.

Hence, we will need another application called `navigation`.
This application will be launching everything we need for
the navigation (localization + navigation).
This application should make sure to load the last map that
we created (with the `mapping` application).
While the mapping is done on rare occasions, the navigation will be rather standard.

Thus, our `navigation` should be running as a daemon in the background.
With the specificity that it should be shipped as disabled (we can enable it)
since we won’t have a map created on the very first install.

#### TurtleBot3 ROS workspace presentation

We have now seen the different applications that TurtleBot3 snap will
have to make its applications easy and error-proof to use.

In the section below we covered the methodology used to define our snap application.
**We must think in terms of functionalities once deployed**.
The usage of a deployed application can differ from the usage that a developer
would have of the same ROS workspace.

It’s now time to look at what’s inside the TurtleBot3 repositories.
This way we will identify how to expand a traditional ROS workspace into
an application-oriented workspace.

In this developer guide, we are going to work with three repositories:
TurtleBot3, TurtleBot3 messages, and TurtleBot3c.

#### TurtleBot3

This is the [official repository from Robotis](https://github.com/ROBOTIS-GIT/turtlebot3/tree/noetic),
which contains most of the TurtleBot3 packages. The main packages for this demo are:

- [Turtlebot3_bringup](https://github.com/ROBOTIS-GIT/turtlebot3/tree/noetic/turtlebot3_bringup):
  Contains robot launch files for different configurations.
- [Turtlebot3_description](https://github.com/ROBOTIS-GIT/turtlebot3/tree/noetic/turtlebot3_description):
  Contains URDF files as well as meshes.
- [Turtlebot3_navigation](https://github.com/ROBOTIS-GIT/turtlebot3/tree/noetic/turtlebot3_navigation):
  Contains launch files and parameters for navigation algorithm and
  ROS packages (AMCL, `move_base`).
- [Turtlebot3_slam](https://github.com/ROBOTIS-GIT/turtlebot3/tree/noetic/turtlebot3_slam):
  Contains launch files and configurations for the different SLAM algorithm
  (gmapping, hector slam, etc.).
- [Turtlebot3_teleop](https://github.com/ROBOTIS-GIT/turtlebot3/tree/noetic/turtlebot3_teleop):
  Containing the node to control TurtleBot3 with a keyboard.

All these ROS packages contain `package.xml`,
effectively listing all the build time and run-time dependencies.
Recall that these `packages.xml` files are used by `snapcraft` plugins to
automatically pull dependencies.
If we were to use a different robot stack we should make sure that similarly,
the `package.xml` is properly listing the dependencies.

Since we are running ROS Noetic for this guide,
we will be using the `noetic-devel` branch along with the corresponding Ubuntu 20.04.

#### TurtleBot3 messages

Additionally, the [`turtlebot3_msgs`](https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git)
repository is another official repository from Robotis and
contains the TurtleBot3 messages definition.
The messages (`Version`, `Sound`, and `SensorState`) are
specific to the TurtleBot3 application.

#### TurtleBot3c

[TurtleBot3c](https://github.com/canonical/turtlebot3c/tree/noetic-devel)
is a collection of configurations/launch files maintained by
the robotics team at Canonical created for this developer guide.
The purpose of this repository is to easily expose applications-oriented `launchfiles`.

It is composed of four different packages:

- [Turtlebot3c](https://github.com/canonical/turtlebot3c/tree/noetic-devel/turtlebot3c):
  The meta-package of this repository.
- [Turtlebot3c_2dnav](https://github.com/canonical/turtlebot3c/tree/noetic-devel/turtlebot3c_2dnav):
  Contains one mapping launch file, and one navigation launch file.
- [Turtlebot3c_bringup](https://github.com/canonical/turtlebot3c/tree/noetic-devel/turtlebot3c_bringup):
  Contains a general bring-up launch file capable of launching
  the basic nodes to interface with the real TurtleBot3 or
  its Gazebo classic simulation.
- [Turtlebot3c_teleop](https://github.com/canonical/turtlebot3c/tree/noetic-devel/turtlebot3c_teleop):
  Contains launch files as well as configuration for
  joystick and keyboard teleoperation.

While the first three packages are rather straightforward,
the [turtlebot3c_teleop](https://github.com/canonical/turtlebot3c/tree/noetic-devel/turtlebot3c_teleop)
package adds logic that is not present in the original TurtleBot3 repository.
We indeed use a topic multiplexer called [topic_tools/mux](https://wiki.ros.org/topic_tools/mux)
responsible for rooting the desired robot control topic to
the `/cmd_vel` topic (see figure below).
This way our TurtleBot3 could be controlled by a joystick, a keyboard,
or even the navigation depending on what we desire without interfering with each other.

![/cmd_vel mux](https://assets.ubuntu.com/v1/c59f2f80-teleop-mux.png)

Selecting the topic which is going to be redirected,
can be done with the following command:

```bash
rosservice call /mux/select "topic: 'key_vel'"
```

## Snapping our software

In the previous section, we have defined the applications that our snap must expose.
We have also seen the different repositories from TurtleBot3 that
we will need to implement those applications.
This is the first step to writing our `snapcraft.yaml` file.

The following section is going to cover how to snap applications, step by step.
The final version of the snap workspace is [available on GitHub](https://github.com/canonical/turtlebot3c-snap/tree/noetic-devel).
We can refer to it at any time in case we have questions
regarding the content of a file.

### Completing our snapcraft.yaml

Let’s create a directory for our project:

```bash
mkdir -p turtlebot3c_snap/

cd turtlebot3c_snap
```

And let's initialise our snap project:

```bash
snapcraft init
```

This will create a `snap/snapcraft.yaml` file.

In this file, we first need to complete the metadata along with [`strict` confinement](https://snapcraft.io/docs/explanation/security/snap-confinement/)
and [`core20`](https://documentation.ubuntu.com/snapcraft/stable/how-to/crafting/specify-a-base/).

```yaml
name: turtlebot3c
base: core20
version: '1'
summary: Turtlebot3c core snap
description: |
  This snap automatically spawns a roscore and the core components for the
  Turtlebot3.
confinement: strict
```

Everything here is self-explanatory.
We start directly from `strict` confinement since we already know that
`network` and `network` bind are the necessary plugs for ROS.

#### Build the workspace

As mentioned in the previous section, we will use three different repositories.
[turtlebot3](https://github.com/ROBOTIS-GIT/turtlebot3/tree/noetic) and
[turtlebot3c](https://github.com/canonical/turtlebot3c) but also
[`turtlebot3_msgs`](https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git)
since TurtleBot3 messages are hosted on a different repository.

Here we will define one [snapcraft part](https://documentation.ubuntu.com/snapcraft/stable/reference/snapcraft-yaml/index.html)
for our ROS workspace.
For this snapcraft part, we will use the [`catkin` plugin](https://documentation.ubuntu.com/snapcraft/8.14/reference/plugins/catkin_plugin/).
As seen in the [previous part of this guide](https://ubuntu.com/robotics/docs/ros-deployment-with-snaps-part-1),
the `catkin` plugin comes in handy with the [`ros-noetic` snapcraft extensions](https://documentation.ubuntu.com/snapcraft/8.14/reference/extensions/ros-1-extension/).

The source is used to retrieve the source tree to build.
Here we have three different GitHub repositories ([turtlebot3](https://github.com/ROBOTIS-GIT/turtlebot3/tree/noetic),
[turtlebot3c](https://github.com/canonical/turtlebot3c) and
[`turtlebot3_msgs`](https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git)).
We cannot put all three in the source entry.
We will use [Vcstool](https://github.com/dirk-thomas/vcstool)
to pull all the repositories that we need based on a
[rosinstall file](https://docs.ros.org/en/independent/api/rosinstall/html/rosinstall_file_format.html).

A detailed explanation of this process can be found in the
[Vcstool and rosinstall file documentation](https://ubuntu.com/robotics/docs/vcstool-and-rosinstall-file).

##### Writing our turtlebot3 part

The very first thing that we need is a `.rosinstall` file.
We will populate this file with our three repositories:

*turtlebot3c.rosinstall*:

```yaml
- git: {local-name: turtlebot3, uri: 'https://github.com/ROBOTIS-GIT/turtlebot3.git', version: noetic-devel}
- git: {local-name: turtlebot3_msgs, uri: 'https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git', version: noetic-devel}
- git: {local-name: turtlebot3c, uri: 'https://github.com/ubuntu-robotics/turtlebot3c.git', version: noetic-devel}
```

We will place this file at the root of our `turtlebot3c_snap` directory.
Right next to the `snap/` folder.

Now we must write the `snapcraft` part to lever this file with the Vcstool.
We will need `python3-vcstool` at build time to use our `rosinstall` file.

Our part to build ROS workspace is going to be:

```yaml
parts:
  workspace:
    plugin: catkin
    source: . # import our rosinstall file
    build-packages: [python3-vcstool, git]
    stage-packages:
      - ros-noetic-rosbash # necessary if we need rosrun
      - ros-noetic-roslaunch # necessary if we need roslaunch
    override-pull: |
      snapcraftctl pull
      # Here we are going to use the local .rosinstall file
      vcs import --input turtlebot3c.rosinstall
```

Here, the [`catkin` plugin](https://documentation.ubuntu.com/snapcraft/8.14/reference/plugins/catkin_plugin/)
is going to use the `package.xml` present in the different source packages to
manage the ROS dependencies.
It will also build and install our packages.

Before running any kind of build, let’s declare our applications.

##### Building the core app

Above, we defined that we needed a `core` daemon responsible to launch the motor controller,
advertising the sensors,
uploading the robot model to the `rosparam` server and
publishing the robot `tf` tree.

In the TurtleBot3c ROS world this corresponds to the launch file [`turtlebot3c_bringup.launch`](https://github.com/canonical/turtlebot3c/blob/noetic-devel/turtlebot3c_bringup/launch/turtlebot3c_bringup.launch)
inside the `turtlebot3_bringup` package (installed by the part we just added).
This application must be running in the background,
we will thus declare it as a `daemon`.
Remember that since it’s a ROS application we will need a ROS environment.
So we will use the
[`ros-noetic` snapcraft extensions](https://documentation.ubuntu.com/snapcraft/8.14/reference/extensions/ros-1-extension/).

In our case, we will define a `core` application that will work with the
[TurtleBot3 waffle_pi model](https://emanual.robotis.com/docs/en/platform/turtlebot3/features/).
In the launch file this is done by defining an environment variable.

The robot is managing all its hardware interfaces through USB.
By default, our snap won’t have access to it.
We then have to declare the [usb-raw plug](https://snapcraft.io/docs/reference/interfaces/raw-usb-interface/).

Let’s add this app to our `snapcraft.yaml`:

```yaml
apps:
  core:
    daemon: simple
    environment:
      TURTLEBOT3_MODEL: waffle_pi
    command: opt/ros/noetic/bin/roslaunch turtlebot3c_bringup turtlebot3c_bringup.launch
    plugs: [network, network-bind, raw-usb]
    extensions: [ros1-noetic]
```

We have introduced a new entry to our app called `environment`.
This way we can define environment variables that are specific to our application.
We can find all the apps and services metadata in the [documentation](https://documentation.ubuntu.com/snapcraft/stable/reference/snapcraft-yaml/index.html).

##### Building the teleop app

Along with `core`,
the `teleop` should be declared as a daemon too since we want it
to be running in the background.
The `teleop` app will be running our teleoperation multiplexer.
This corresponds to the launch file [`turtlebot3c_teleop.launch`](https://github.com/canonical/turtlebot3c/blob/noetic-devel/turtlebot3c_teleop/launch/turtlebot3c_teleop.launch)
in the `turtlebot3c_teleop` package.

We can declare this application by adding the following to our `snapcraft.yaml`:

```yaml
apps:
  [...]
  teleop:
    daemon: simple
    command: opt/ros/noetic/bin/roslaunch turtlebot3c_teleop turtlebot3c_teleop.launch
    plugs: [network, network-bind]
    extensions: [ros1-noetic]
```

This application is highly similar to the `core` app. Nothing to declare.

#### Building the key app

Using the above `teleop` application and adding a `key` application would
let us effectively teleoperate the TurtleBot3.
Here the `key` application will be a command to call.

This app must publish a `/key_vel` topic based on the keyboard input.
This corresponds to the [`key.launch`](https://github.com/canonical/turtlebot3c/blob/noetic-devel/turtlebot3c_teleop/launch/key.launch)
from the `turtlebot3c_teleop` package.
Snaps are by default accessing the keyboard,
so we won’t need any special `plugs` here.

We then add the following to our `snapcraft.yaml`:

```yaml
apps:
  [...]
  key:
    command: opt/ros/noetic/bin/roslaunch turtlebot3c_teleop key.launch
    plugs: [network, network-bind]
    extensions: [ros1-noetic]
```

Again this is very straightforward with what we have already done.

With this new application,
our snap will now make a command available called `turtlebot3c.key`.

##### Building the joy app

Very similar in terms of usage to `key`,
but we will use a different launch file for the joystick.
It’s [`joy.launch`](https://github.com/canonical/turtlebot3c/blob/noetic-devel/turtlebot3c_teleop/launch/joy.launch)
from the `turtlebot3c_teleop` package.
The major differences are that this is going to be published on the
`/joy_vel` topic and
that our application will need access to the joystick.
We must use the [`joystick` interface](https://snapcraft.io/docs/reference/interfaces/joystick-interface/),
so our confined application will be able to access the joystick device from our host.

We then add the following to our `snapcraft.yaml`:

```yaml
apps:
  [...]
  joy:
    command: opt/ros/noetic/bin/roslaunch turtlebot3c_teleop joy.launch
    plugs: [network, network-bind, joystick]
    extensions: [ros1-noetic]
```

With this new application,
our snap will now make a command available called `turtlebot3c.joy`.

Now we have all the applications necessary for teleoperation whether
we want to use a keyboard or a joystick.

##### Building the mapping app

For the mapping,
we will need a command that we can call whenever we want to start doing a mapping.
This command `mapping` is going to rely on the [`turtlebot3c_mapping.launch`](https://github.com/canonical/turtlebot3c/blob/noetic-devel/turtlebot3c_2dnav/launch/turtlebot3c_mapping.launch)
file from the `turtlebot3c_2dnav` repository.
This is also straightforward.

We add the following to our `snapcraft.yaml`:

```yaml
apps:
  [...]
  mapping:
    environment:
      TURTLEBOT3_MODEL: waffle_pi
    command: opt/ros/noetic/bin/roslaunch turtlebot3c_2dnav turtlebot3c_mapping.launch
    plugs: [network, network-bind]
    extensions: [ros1-noetic]
```

With this new application,
our snap will now make a command available called `turtlebot3c.mapping`.

Note that the [`turtlebot3c_mapping.launch`](https://github.com/canonical/turtlebot3c/blob/noetic-devel/turtlebot3c_2dnav/launch/turtlebot3c_mapping.launch)
accepts ROS arguments to select a different SLAM algorithm.
This is nicely compatible with our snap application,
and we could imagine calling our application with the argument:

```bash
turtlebot3c.mapping slam_methods:=hector
```

##### Building the navigation app

Finally, our last application, `navigation`.
`navigation` will also be a daemon running in the background but with one specificity.
It’s not going to be enabled at first.
The reason is that when we first install our snap, we won’t have created any map.
This way we can create our first map and then activate our navigation daemon.
Daemons can be installed in a disabled state thanks to
the additional app entry: `install-mode: disable`.
Once enabled it will remain enabled even after an update.

The whole navigation stack relies on
[`turtlebot3c_navigation.launch`](https://github.com/canonical/turtlebot3c/blob/noetic-devel/turtlebot3c_2dnav/launch/turtlebot3c_navigation.launch)
from the package `turtlebot3c_2dnav`.
It will launch the localization as well as the navigation.

Let’s add the following to our `snapcraft.yaml`:

```yaml
apps:
  [...]
  navigation:
    environment:
      TURTLEBOT3_MODEL: waffle_pi
    daemon: simple
    install-mode: disable
    command: opt/ros/noetic/bin/roslaunch turtlebot3c_2dnav turtlebot3c_mapping.launch
    plugs: [network, network-bind]
    extensions: [ros1-noetic]
```

Once our snap is installed, we will be able to enable this daemon with the command:

```bash
sudo snap start --enable turtlebot3c.navigation
```

## Application scripts

So far we have defined our part as well as our different applications in our snap.
Nothing there was new.
It was simply an application of the basic ROS/snap knowledge to the TurtleBot3 case.

Let’s say that we want our snap `navigation` daemon to
always use the latest recorded map.
Or that we want the mapping to automatically save the map without
having to manually call a ROS service to save the map.

For these, we can use additional features of `snap` and `snapcraft`.
These features will make our applications much more
integrated and easier for the final user.
The features that we will describing below are:

- Environment variables.
- Local file parts.
- Launcher scripts.
- Daemon scripts.

### Snap environment variables

Environment variables are widely used across Linux to provide convenient access
to system and application properties.
Both `snapcraft` and `snapd` consume, set,
and pass-through specific environment variables to support building and running snaps.

There are snap environment variables,
like `$SNAP` and `$SNAP_INSTANCE_NAME` used to identify the snap and its location.
The [*Snap environment variables*](https://ubuntu.com/robotics/docs/snap-environment-variables)
documentation is a great place to learn about these.

Additionally, snaps define environment variables specific to data and file storage.
The [*Snap data and file storage documentation*](https://ubuntu.com/robotics/docs/snap-data-and-file-storage)
is a great place to learn about these.

### Local files part

In order to create additional behaviour for a snap, we need to add scripts.
These scripts could be for example responsible for calling
the ROS node in charge of saving the map.

To import all these local files into our snap we will need an additional
`snapcraft` [part](https://documentation.ubuntu.com/snapcraft/stable/reference/snapcraft-yaml/index.html).
They are used to declare pieces of code that will be pulled into your snap package.

So far we only have one part called `workspace` using our `rosinstall` file to
build and install our ROS repository.
This part is relying on the [`catkin` plugin](https://documentation.ubuntu.com/snapcraft/8.14/reference/plugins/catkin_plugin/).

In order to simply import scripts into our snap we will need a different plugin,
the [`dump` plugin](https://documentation.ubuntu.com/snapcraft/stable/common/craft-parts/reference/plugins/dump_plugin/).

As its name suggests, the `dump` plugin is simply used to
"dump" the specified sources in a specified location into our snap.
Usually, the dumped files are scripts, configuration files, binaries etc.

### Adding scripts to our snap’s part

In our case we will simply need to dump all the files that we are going to
store in `snap/local` into the `usr/bin` of our snap.

We will then need to add the following part to the `snapcraft.yaml`:

```diff
parts:
  workspace:
    [...]
+ # copy local scripts to the snap usr/bin
+ local-files:
+   plugin: dump
+   source: snap/local/
+   organize:
+     '*.sh': usr/bin/
```

The organize keyword is a key/value pair,
the key represents the path of a file inside the selected source of
the part and the value represents the file's destination in the stage area.

### Launcher scripts

Now we have a part to import local files, but we don’t have the local files yet.

So far for our `snapcraft` apps, in the `command` entry,
we have been writing the full name of the commands.
For example, for our `core` application, we wrote:

```yaml
command: /opt/ros/noetic/bin/roslaunch turtlebot3c_bringup turtlebot3c_bringup.launch
```

Our [turtlebot3c_bringup.launch](https://github.com/canonical/turtlebot3c/blob/noetic-devel/turtlebot3c_bringup/launch/turtlebot3c_bringup.launch#L21)
is actually taking a `simulation` argument.
It can be set to `false` or `true`,
to specify whether we want to run the bring-up for the simulation or not.
Since the core application is a daemon,
we cannot append anything to the specified command at launch.
This means that we must give it directly in the command.

By trying we will quickly realise that we are facing an issue.
The character “=” is forbidden in the `snapcraft.yaml`.
To specify an argument to a ROS launch file we must
use the syntax `arg_name:=arg_value`.
For this reason (and actually many others that we will discuss later on)
our snapcraft command entry is going to call a script
containing a call to our command.

This way, we will not only be able to specify ROS arguments,
but we will also be able to potentially perform some simple checks or
any kind of behaviour that would not be that easy on a one-liner.
For example, verifying that a file exists before calling a command.

#### Adding scripts’ launcher

For our TurtleBot3 snap, we will add a launcher script for `core`,
`mapping` and `navigation`.

Let’s add these scripts into our snap/local folder.

First, we create the folder:

```bash
mkdir -p snap/local
```

Then we add the file:
*snap/local/core_launcher.sh*:

```bash
#!/usr/bin/bash

${SNAP}/opt/ros/noetic/bin/roslaunch turtlebot3c_bringup turtlebot3c_bringup.launch simulation:=true
```

Here we are using the `$SNAP` variable that we saw earlier.
This way we are sure of the binary that we are calling.
Also, we are assigning the `simulation` argument to `true`.
We will see [in the next section](#turtlebot3-configurations)
how to make it configurable.

Similarly, the next two scripts:

*snap/local/mapping_launcher.sh*:

```bash
#!/usr/bin/bash

${SNAP}/opt/ros/noetic/bin/roslaunch turtlebot3c_2dnav turtlebot3c_mapping.launch
```

*snap/local/navigation_launcher.sh*:

```bash
#!/usr/bin/bash

${SNAP}/opt/ros/noetic/bin/roslaunch turtlebot3c_2dnav turtlebot3c_navigation.launch
```

Since these three scripts are going to be executed. Let’s turn them into executables:

```bash
chmod +x snap/local/*.sh
```

#### Using scripts

Now, let’s use these scripts in our `snapcraft.yaml` instead of the “raw” commands.
Remember that with the new part we added: “`local-files`”,
our scripts are going to be staged into `usr/bin`.

```diff
apps:
  core:
    [...]
-   command: opt/ros/noetic/bin/roslaunch turtlebot3c_bringup turtlebot3c_bringup.launch
+   command: usr/bin/core_launcher.sh
    [...]
  mapping:
    [...]
-   command: opt/ros/noetic/bin/roslaunch turtlebot3c_2dnav turtlebot3c_mapping.launch
+   command: usr/bin/mapping_launcher.sh
    [...]
  navigation:
    [...]
-   command: opt/ros/noetic/bin/roslaunch turtlebot3c_2dnav turtlebot3c_mapping.launch
+   command: usr/bin/navigation_launcher.sh
```

Our `snapcraft.yaml` is now using scripts for the commands.
They are the first scripts of our snaps since many are coming.
For now, we might think that those scripts are a complexity we could avoid.
But in the next sections, we will see that we will greatly need them.

#### Daemon scripts

In TurtleBot3 we already have a few daemons.
These snap services can use multiple new features that
will come in handy for our application.

`Snap` and `snapcraft` offer great features to orchestrate daemon applications.
The [*Application orchestration*](https://ubuntu.com/robotics/docs/application-orchestration)
documentation is a great place to learn more about orchestration.

The orchestration features that we are going to use for the TurtleBot3 are:

- Command-chain
  - We will use it to select the right multiplexer topic for controlling the robot.
- Stop-command
  - We will use it for our `mapping` application.
    This way we will trigger the save of the map whenever we exit the mapping.
    No more maps lost that took forever to create!
- Post-stop-command
  - We will use it to “install” the map for our `navigation` application.
    This way the `navigation` will always use the last created map.

#### Applying daemon scripts to TurtleBot3

We have already made our applications run in the background,
it’s now time to automate and simplify our user experience.

Here we want to make the map creation and use as simple as it can be.
We don’t want the user to have to call ROS nodes manually or
even manipulate map files by himself.

To achieve this we will:

1. Save the map whenever we stop the `mapping`.
2. Use only the last map we created for the `navigation`
  without having to specify the new map name.
3. Verify that a map is available before starting our navigation stack.
4. Make the velocity command multiplexer automatically select the correct topic
  depending on the command we are using.

These are basic functionalities that our applications need to automate and
simplify the user experience.
Similarly, your application could also require implementing similar features.

#### Save the map

When the `mapping` is running,
to save the map we will have to call the following ROS node:

```bash
rosrun map_server map_saver -f "PATH_AND_NAME_OF_THE_FILE"
```

Having to run it manually is, first, more work,
but also the user must provide the correct path.
Let’s make this automatic!

The `stop-command` will be the perfect feature to call our map server.
The only thing is that our `mapping` is currently a command.
To use `stop-command` we will have to turn it into a daemon.

Let’s modify our `snapcraft.yaml`:

```diff
apps:
  [...]
  mapping:
    environment:
      TURTLEBOT3_MODEL: waffle_pi
    command: usr/bin/mapping_launcher.sh
+   daemon: simple
+   install-mode: disable
+   stop-command: usr/bin/save_map.sh
    plugs: [network, network-bind]
    extensions: [ros1-noetic]
```

Now our `mapping` is a daemon (disabled by default,
so it doesn’t start by itself on the first install).
It will launch a script called `save_map.sh` that we will create right now.

The script is simply going to run the map saver in the `$SNAP_USER_COMMON`
directory (read/write directory kept over the updates).
Let’s create the file `snap/local/save_map.sh`:

```bash
#!/usr/bin/bash

# make map directory if not existing
mkdir -p ${SNAP_USER_COMMON}/map

$SNAP/opt/ros/noetic/bin/rosrun map_server map_saver -f "${SNAP_USER_COMMON}/map/new_map"
```

Now our map will be saved automatically whenever we stop our
mapping service (with the `sudo snap stop mapping` command).
The current limitation here is that every map that we create is called `new_map`.
It would be better to keep all the maps created and simply mark one as the current one.
This way we could even restore a previous one later.

#### Install the last map

Here we are going to make sure that we keep every map and
also that `current_map` is always pointing to the last created map.
This way our navigation will always load the same symlink file but
always point to the latest map.
To do so we will have to create a script installing the last map and
execute it as a `post-stop-command`.
Once the `stop-command` and our service is stopped our map is created,
and it’s time to install it.

Let’s modify our `snapcraft.yaml` to add the `post-stop-command`:

```diff
apps:
  [...]
  mapping:
    [...]
+   stop-command: usr/bin/save_map.sh
    post-stop-command: usr/bin/install_last_map.sh
    plugs: [network, network-bind]
    extensions: [ros1-noetic]
```

Now let’s create our `install_last_map.sh` script in `snap/local`:

```bash
#!/usr/bin/bash
set -e
# backup our map with the date and time
DATE=`date +%Y%m%d-%H-%M-%S`
mv ${SNAP_USER_COMMON}/map/new_map.yaml ${SNAP_USER_COMMON}/map/$DATE.yaml
sed -i "s/new_map.pgm/$DATE.pgm/" ${SNAP_USER_COMMON}/map/$DATE.yaml
mv ${SNAP_USER_COMMON}/map/new_map.pgm ${SNAP_USER_COMMON}/map/$DATE.pgm

# create symlink to use the map
rm -f ${SNAP_USER_COMMON}/map/current_map.yaml
ln -s ${SNAP_USER_COMMON}/map/$DATE.yaml ${SNAP_USER_COMMON}/map/current_map.yaml
```

Here we move the freshly created map files (prefixed with `new_map`) to
new file names based on date.
Finally, we create a UNIX symlink to point to the last map.
This way we keep track of every map created and when it was created.
Our navigation service is already loading the file
`${SNAP_USER_COMMON}/map/current_map.yaml`.
So by loading the symlink our `navigation` is always going to load the last created map.

#### Navigation launcher adaptation

Here we are simply going to adapt our navigation launcher to
verify that our map file exists before launching the navigation launch file.

We already created the `navigation_launch.sh` script in `snap/local`:

```diff
#!/usr/bin/bash
+if [ -f "${SNAP_USER_COMMON}/map/current_map.yaml" ]; then
   ${SNAP}/opt/ros/noetic/bin/roslaunch turtlebot3c_2dnav turtlebot3c_navigation.launch
+else
+  >&2 echo "File ${SNAP_USER_COMMON}/map/current_map.yaml does not exist." \ "Have you run the mapping application?"
+fi
```

The script is simply checking if the file `${SNAP_USER_COMMON}/map/current_map.yaml`
exists and launches the navigation.
Otherwise, we simply log an error message.

#### Velocity multiplexer selection

In the first sections of this guide,
we described that a multiplier has been set to forward only one topic
(`/joy_vel`, `/key_vel` or `/nav_vel`).
Once selected the topic is forwarded to `/cmd_vel`.
To select a topic we must call a ROS service with the command:

```bash
rosservice call /mux/select "/joy_vel"
```

Every time we call the `key` command (to start the keyboard teleoperation)
we will have to call the ROS service to select our `/key_vel` topic.

Let’s make this automatic every time we start any
of the applications that need a specific topic.
We are talking about `key`, `joy` and `navigation`.

Let’s add a `command-chain` in our `snapcraft.yaml` calling a
selection script for all our apps that need it.

```diff
apps:
  [...]
  key:
+   command-chain: [usr/bin/mux_select_key_vel.sh]
    command: opt/ros/noetic/bin/roslaunch turtlebot3c_teleop key.launch
  [...]
  joy:
+   command-chain: [usr/bin/mux_select_joy_vel.sh]
    command: opt/ros/noetic/bin/roslaunch turtlebot3c_teleop joy.launch
  [...]
  navigation:
+   command-chain: [usr/bin/mux_select_nav_vel.sh]
    command: usr/bin/navigation_launcher.sh
```

Now let’s add the different scripts:

*snap/local/mux_select_key_vel.sh*:

```bash
#!/usr/bin/bash
$SNAP/opt/ros/noetic/bin/rosservice call /mux/select "/key_vel"
exec $@
```

*snap/local/mux_select_joy_vel.sh*:

```bash
#!/usr/bin/bash
$SNAP/opt/ros/noetic/bin/rosservice call /mux/select "/joy_vel"
exec $@
```

*snap/local/mux_select_nav_vel.sh*:

```bash
#!/usr/bin/bash
$SNAP/opt/ros/noetic/bin/rosservice call /mux/select "/nav_vel"
exec $@
```

Note that the exec `$@` is necessary at the end of our `command-chain`
scripts since our actual command is given as an argument of the `command-chain`.
Now with the help of our `command-chain` scripts whenever we start the
`joy` app (or another controlling app) we are ready to control the
robot with any additional commands.

## Turtlebot3 configurations

In the previous section,
we have seen how to add advanced behaviour to our snap by
leveraging new `snapcraft` YAML keywords.
Our final TurtleBot3 snap application must cover multiple cases.
It should work with all the flavours of TurtleBot3 as well as
with the simulation and the real robot.

Adding such behaviour is going to require a new feature from snap: `hooks`.
`Hooks` are executable files that run within a snap’s confined environment
when a certain action occurs.
They are typically used for configurations.
The documentation on [*snap configurations and hooks*](https://ubuntu.com/robotics/docs/snap-configurations-and-hooks)
explains this in detail.

### Adding TurtleBot3 hooks

Here there are multiple things that we want to achieve:

- Our snap must be working for the simulation but also for the real robot.
  We will need a `simulation` configuration.
- TurtleBot3s come in different flavours: `burger`, `waffle` and `waffle_pi`.
  We will then also need a `turtlebot3-model` configuration.
- We will have to declare hooks to define our configurations and
  make sure the new value matches the requirements.
- Additionally, we will integrate those new parameters into our different scripts.

#### Simulation parameter

For the simulation,
the only application that is going to be impacted is the `core` daemon.
Since the snap is not meant to run the simulation itself but
simply to interface with it,
there is no big challenge here.

For this first parameter, we will have to create the hook scripts first.

##### Hooks

The very first hook that we are going to define is [`The install hook`](https://snapcraft.io/docs/reference/development/supported-snap-hooks/#heading--install).
This hook is called upon initial installation only.
We are going to use the `The install hook`  to declare our parameter default value.

First we create the directory:

```bash
mkdir -p snap/hooks
```

Let’s create a file called `install` inside the directory `snap/hooks` and
add the following content:

```bash
#!/bin/sh -e
# set default configuration values
snapctl set simulation=false
```

We used `snapctl` to set the default value to false.

Additionally,
we are going to create a file called `configure` in the `snap/hooks` directory.

Add the following content to `snap/hooks/configure`:

```BASH
#!/bin/sh -e
SIMULATION="$(snapctl get simulation)"
case "$SIMULATION" in
  "true") ;;
  "false") ;;
  "0") ;;
  "1") ;;
  *)
    >&2 echo "'$SIMULATION' is not a supported value for simulation." \ "Possible values are true, false, 0, 1"
    return 1
    ;;
esac

# restart core and teleop on new config
snapctl stop "$SNAP_INSTANCE_NAME.core"
snapctl stop "$SNAP_INSTANCE_NAME.teleop"
snapctl start "$SNAP_INSTANCE_NAME.core"
snapctl start "$SNAP_INSTANCE_NAME.teleop"
```

Here again we used `snapctl`.
We use it to read the parameter and make sure it contains a valid value
(in our case: `true`, `false`, `0` or `1`).
In case the value is wrong we simply return an error.

Additionally,
we made sure to restart our `core` and `teleop` daemons (meant to be always running).
This way when we change a parameter we are sure that it is
taken into consideration immediately.

Since our hooks are scripts we must make sure to make them executable.
We can do so with:

```bash
chmod +x snap/hooks/*
```

##### Use the configuration

Now that our snap is defining our configuration we must use it in our application.

Let’s modify our `core_launcher.sh` script located in `snap/local`:

```diff
#!/usr/bin/bash
+SIMULATION="$(snapctl get simulation)"
-${SNAP}/opt/ros/noetic/bin/roslaunch turtlebot3c_bringup turtlebot3c_bringup.launch simulation:=true
+${SNAP}/opt/ros/noetic/bin/roslaunch turtlebot3c_bringup turtlebot3c_bringup.launch simulation:=$SIMULATION
```

This way we read the snap configuration to store it into a variable and
finally use it as a ROS argument for our launch file.

This way, when changing the configuration of the snap with the command:

``` bash
sudo snap set turtlebot3c simulation=true
```

Our `configure` script is going to be called,
restarting the `core` daemon.
And finally our `core_launcher.sh` is going to be started with the correct configuration.

#### Turtlebot3 model

The TurtleBot3 has several hardware configurations.
These models are `burger`, `waffle`, and `waffle_pi`.
The different models are available for the real robot but also for the simulation.
While we will mostly work with the `waffle_pi` simulation,
the others can also be tested easily.
Similarly, we will complete our hooks and
the different scripts where we must specify the model.

##### Hooks

First, let’s define the default value for our configuration `turtlebot3-model`.
Let’s add our configuration to the `snap/hooks/install` file:

```diff
snapctl set simulation=false

+# set default turtlebot 3 model
+snapctl set turtlebot3-model=waffle_pi
```

Similarly, we must complete the `snap/hooks/configure` hook:

```diff
+TURTLEBOT3_MODEL="$(snapctl get turtlebot3-model)"
+case "$TURTLEBOT3_MODEL" in
+  "burger") ;;
+  "waffle") ;;
+  "waffle_pi") ;;
+  *)
+    >&2 echo "'$TURTLEBOT3' is not a supported value for turtlebot3-model." \
+"Possible values are burger, waffle and waffle_pi"
+    return 1
+    ;;
+esac

# restart core and teleop on new config
snapctl stop "$SNAP_INSTANCE_NAME.core"
snapctl stop "$SNAP_INSTANCE_NAME.teleop"
```

Now, our hooks are correctly handling the `turtlebot3-model` configuration.
Nothing new here we have applied what we used for the other configuration.

###### Use the configuration

Now let’s use the robot model configuration for our applications.
So far we have specified the robot model via
the `environment` keyword in our application.
This is no longer possible since we now need to
use `snapctl` to read our configuration.
The TurtleBot3 model is read [by the mean of an environment variable](https://github.com/ROBOTIS-GIT/turtlebot3/blob/noetic/turtlebot3_bringup/launch/turtlebot3_robot.launch#L4).
We will then have to remove the hard-coded environment variable in
our `snapcraft.yaml` and define it in our different launcher scripts.

First, let’s remove the hard-coded one in our `snapcraft.yaml`:

```diff
apps:
  core:
-   environment:
-   TURTLEBOT3_MODEL: waffle_pi
  [...]
  mapping:
-   environment:
+     TURTLEBOT3_MODEL: waffle_pi
  [...]
  navigation:
-   environment:
-     TURTLEBOT3_MODEL: waffle_pi
```

Now let’s define this `TURTLEBOT3_MODEL` in the launcher scripts that need it.
The first one is the `core` daemon.
We can modify `snap/local/core_launcher.sh` this way:

```diff
SIMULATION="$(snapctl get simulation)"
+TURTLEBOT3_MODEL="$(snapctl get turtlebot3-model)"

+export TURTLEBOT3_MODEL
```

We read the parameter and then simply export the environment variable.

Now let’s do the same thing but to the `navigation` and
`mapping` launcher script: *snap/local/mapping_launcher.sh*.

```diff
+TURTLEBOT3_MODEL="$(snapctl get turtlebot3-model)"
+export TURTLEBOT3_MODEL
${SNAP}/opt/ros/noetic/bin/roslaunch turtlebot3c_2dnav turtlebot3c_mapping.launch
```

And *snap/local/navigation_launcher.sh*:

```diff
+TURTLEBOT3_MODEL="$(snapctl get turtlebot3-model)"
+export TURTLEBOT3_MODEL
if [ -f "${SNAP_USER_COMMON}/map/current_map.yaml" ]; then
```

Then we can make sure that all these scripts are executable:

```bash
chmod +x snap/local/*
```

From now on, we can select an alternative TurtleBot3 model with the simple command

```bash
sudo snap set turtlebot3c turtlebot3-model=burger
```

We have finally finished defining all our snap hooks.
Additionally, we have implemented every application and
functionality we need for our snap.
It’s time to build it and test it!

We will run all our tests in simulation,
but with a TurtleBot3 robot available we could also test it on the real robot.

### Final test

We can now do a final test of everything we achieved so far.

Since we did multiple tests, our writable directories already have data.
To reproduce the first install of our snap, we can remove and purge our snap.
This will not only remove our snap and previous revisions,
but it will also clean all its data.

To do so:

```bash
sudo snap remove turtlebot3c --purge
```

We can now proceed to a complete test, from installation to navigation.
Let’s go through the following steps:

1. Install the snap:

   `sudo snap install turtlebot3c_*.snap --dangerous`
2. Set the simulation parameter

    `sudo snap set turtlebot3c simulation=true`
3. Start the simulation

    `TURTLEBOT3_MODEL=waffle_pi roslaunch turtlebot3_gazebo turtlebot3_world.launch`
4. Start the `mapping`

   `sudo snap start turtlebot3c.mapping`

5. Roam around with the `key` application

   `turtlebot3c.key`

6. Stop the `mapping`

   `sudo snap stop turtlebot3c.mapping`

7. Start the `navigation`

   `sudo snap start turtlebot3c.navigation`

8. Start `RViz`

    `rviz -d /opt/ros/noetic/share/turtlebot3_slam/rviz/turtlebot3_gmapping.rviz`

9. Test the navigation

We now have a complete snap that is completely tested.
We created a map,
we can now make sure the `navigation` daemon starts automatically
at boot by enabling the service.
Let’s call the following command.

```bash
sudo snap start --enable turtlebot3c.navigation
```

In case we want all the `turtlebot3c` daemons to stop and not start again,
we can disable the snap with:

```bash
sudo snap disable turtlebot3c
```

This will prevent any application and daemons from starting.
Additionally, it will also prevent updates.

By checking the output of:

```bash
snap info turtlebot3c
```

We can confirm that all the daemons are stopped and disabled.
Of course, we can enable it later with the snap enable command.

We have now presented every single step to snap a TurtleBot3 software stack.
We went from application identification to actual snapping and
finally added some advanced behaviour to automatize the map management tasks.

## Exercise

Now that we have learned the ins and outs of the TurtleBot3 snap,
we can apply some of our fresh knowledge for a quick exercise.
The exercise as well as the solution are available in the
{ref}`Developer guide part 2 - exercise <tutorials-snaps-core-exercises-exercise-2>`.

```{eval-rst}

   .. toctree::
      :hidden:
      :maxdepth: 1

      Part 2 exercise <exercises/exercise_2.md>
```

-----------------------------

## Next Steps: Debugging

>Now that we've explored and integrated all the new Snap features,
our TurtleBot3 snap is feature-complete and ready for testing.
We've defined our various `parts` and `apps` in the `snapcraft.yaml`,
set up hooks for configuration management,
and implemented scripts to simplify app launches and map creation.
The next step is to thoroughly test the snap using
the simulation with the TurtleBot3 `waffle_pi` model.
>
>Below is a how-to guide focusing on debugging the snap itself and
troubleshooting any issues with how the snap is packaged and
how its components interact,
rather than debugging the code behaviour or compilation errors.
This will help us identify any potential problems with
the snap’s configuration and ensure a smooth user experience.
>
>What we achieved here is perfectly working.
If you would like to learn more about how to debug possible issues,
please refer to the {ref}`how-to guide: Debugging Snap Applications <how-to-guides-packaging-debugging-snap-applications>`.

## Conclusion

We are reaching the conclusion of this developer guide.
This developer guide addressed almost any topic that one might need to
ship a robot software as a snap.

The final version of the snap workspace is [available on GitHub](https://github.com/canonical/turtlebot3c-snap/tree/noetic-devel).
This is the official code that is used to publish the [TurtleBot3c snap](https://snapcraft.io/turtlebot3c)
from the store.
This means that the GitHub repository will keep getting updated.

### What we achieved

In this developer guide,
 we went through the creation of the TurtleBot3 snap.
We have covered all the steps that one must go through when creating a snap for a robot.

First, we identified the different applications and
daemons that our snap must expose.
We also identified the scope of our snap.
Then we applied the knowledge of the first part of the developer guide to
build the first draft of our snap.
By discovering new features of snaps we were able to implement features to
manage our maps and to select the right velocity topic.
We implemented these features to simplify and automate the usage of the snap.

We finally covered the snap debugging aspect.
This helped us to solve all the different issues we encountered while testing the snap.

Now the whole stack of TurtleBot3 for the simulation or
the real robot is packed in a single snap.
