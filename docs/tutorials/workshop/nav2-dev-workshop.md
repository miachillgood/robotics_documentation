(tutorials-workshop-nav2-dev-workshop)=

# Customize a workshop for a project

% Include start summary

In this follow-up tutorial,
we will see how one can further customize a
ROS 2-ready workshop for a specific project.

% Include stop summary

Since this builds upon the
{ref}`Getting started with Workshop <tutorials-workshop-ros2-dev-getting-started>` tutorial,
make sure to complete it first.
There,
we've seen that we can use predefined SDKs to set up
ready-to-use development environment.
More specifically we used the `ros2-desktop` environment to create a ROS 2-ready workshop.

In this follow-up tutorial,
we are going to further customize the development environment
for the specific project we are working with.
While we used the ROS 2 demos repository in part 1,
we are going to use the
[Nav2](https://github.com/ros-navigation/navigation2)
project here since it is better suited to demonstrate the customization feature.

## Setting up

Let us start by cloning the repository:

```console
git clone git@github.com:ros-navigation/navigation2.git --branch jazzy
cd navigation2
```

```{note}
Note that we used the SSH git remote.
We will come back to this detail at the end of this tutorial.
```

Then, create a hidden `.workshop` sub-folder at the project root directory.
We are going to put everything related to Workshop there
in order to keep our project tidy:

```console
mkdir .workshop
touch .workshop/nav2-dev.yaml
```

At this point, the workshop definition is straightforward and only contains
the ROS 2 SDK:

```yaml
name: nav2-dev
base: ubuntu@24.04
sdks:
  - name: ros2-desktop
    channel: jazzy/stable
```

We have now a generic ROS 2-ready workshop definition,
let's customize it to the Nav2 project needs.

## Initiating an in-project SDK

In order to tweak the development environment,
we are making use of an
[in-project SDK](https://ubuntu.com/workshop/docs/explanation/sdks/concepts/#in-project-sdks).
An in-project SDK is an SDK that is distributed alongside a project rather than being
available from the Store.

We proceed to create the in-project SDK:

```console
mkdir .workshop/nav2-sdk
touch .workshop/nav2-sdk/sdk.yaml
```

We then populate the `sdk.yaml` file as follows:

```yaml
name: nav2-sdk
title: ROS 2 Navigation SDK
base: ubuntu@24.04
version: "0.1"
summary: ROS 2 Navigation Framework and System
description: |
  Nav2 provides perception, planning, control, localization, visualization, behaviors,
  and much more to build highly reliable autonomous systems.
  It will compute an environmental model from raw or pre-processed sensor and semantic data,
  dynamically route a path through the environment, compute feasible motor commands,
  avoid obstacles, and structures higher-level robot behaviors. Powered by Open Navigation LLC.
license: LGPL-2.1
platforms:
  amd64:
  arm64:
```

This content is mostly boiler-plate and should be self-explanatory at this stage.

At this point we have a valid in-project SDK, readily usable,
albeit empty.

While we could already launch or refresh our workshop,
the `nav2-sdk` SDK would not change anything at the moment.
So let us keep going.

In-project SDKs are not packaged like other SDKs and
therefore do not make use of `parts`.
They entirely rely on `hooks`.

## Creating the SDK hooks

Let us create the SDK hooks:

```console
mkdir .workshop/nav2-sdk/hooks
touch .workshop/nav2-sdk/hooks/{setup-base,setup-project}
```

Those hooks, `setup-base` and `setup-project` are shell scripts
that are executed to install and configure the SDK content.
They differ in mostly two main aspects:

| | `setup-base` | `setup-project` |
| --- | --- | --- |
| when | before the project is mounted | after the project is mounted |
| who | as `root` | as user |

From these differences,
we can infer that we use the former to install any necessary dependencies,
set up the overall environment, and the second for
user-specific configurations.

Let us look at the `setup-base` hook first:

```bash
_WORKSHOP_ROS_DISTRO='jazzy'

RTI_NC_LICENSE_ACCEPTED=yes \
  apt-get --no-install-recommends --no-install-suggests -y install \
  python3-pip \
  "ros-${_WORKSHOP_ROS_DISTRO}-rmw-fastrtps-cpp" \
  "ros-${_WORKSHOP_ROS_DISTRO}-rmw-connextdds" \
  "ros-${_WORKSHOP_ROS_DISTRO}-rmw-cyclonedds-cpp"
```

In this hook, we make sure that the tier-1 DDS options are installed.
This allows us to test them all,
making sure that our project is DDS vendor agnostic.

Note also that we're not using `sudo` since this script is run as `root`.

And that's actually all for this hook.
Let us move on to the `setup-project` hook that's a little more interesting.

The Nav2 project keeps a list of other ROS 2 projects it requires
in the form of a
[vcstool configuration file](https://github.com/dirk-thomas/vcstool).
Depending on the context, some of those projects may not be available and
it is then necessary to build them from source.
That's what we are going to do in the `setup-project` hook.

Let us look at it:

```bash
_WORKSHOP_ROS_DISTRO='jazzy'

if [ ! -f "/project/tools/underlay.repos" ]; then
  echo "Could not find underlay.repos file in project."
  echo "Aborting setting up the underlay workspace."
  exit 0
fi

set +u
source "/opt/ros/${_WORKSHOP_ROS_DISTRO}/setup.bash"
set -u

rosdep update --rosdistro=${_WORKSHOP_ROS_DISTRO}

# Create underlay workspace
mkdir -p ~/underlay_ws/src
cd ~/underlay_ws/src
vcs import ./ < /project/tools/underlay.repos

# Install underlay workspace's dependencies
# Allow to fail without aborting workshop launch
set +e
rosdep install -q --default-yes --skip-keys slam_toolbox --ignore-src \
  --from-paths ~/underlay_ws/src
set -e

# Build underlay workspace
colcon build \
  --build-base ~/underlay_ws/build \
  --install-base ~/underlay_ws/install \
  --test-result-base ~/underlay_ws/build \
  --symlink-install \
  --mixin release ccache lld \
  --event-handlers console_direct+

# Add setup script to .profile so that it is avail for both interactive and non-interactive shell
if ! grep -q "${HOME}/underlay_ws/install/local_setup.sh" "${HOME}/.profile"; then
  echo "
# Source underlay_ws
if [ -f "${HOME}/underlay_ws/install/local_setup.sh" ]; then
  source "${HOME}/underlay_ws/install/local_setup.sh"
fi
" >> "${HOME}/.profile"
fi
```

This may look complex at first glance, so let's break it down.
The script:

- checks that the Vcstool file to import exists, then exits if it doesn't
  or proceeds otherwise
- sources the ROS 2 environment
- updates Rosdep for good measure
- creates the underlay workspace and import the sources
- installs the underlay workspace dependencies using Rosdep
- builds the underlay workspace using Colcon
- sources the underlay workspace in the user `.profile` file

All this makes sure that a workshop is ready for developing Nav2
the moment it is launched.

Let us put it to the test.

## Launch a Nav2 workshop

With the `nav2-sdk` fully set,
we can launch a workshop tailored for the Nav2 project.

First, let's integrate it to the workshop definition.
We edit our workshop definition file which we renamed `nav2-dev.yaml` earlier:

```diff
name: nav2-dev
base: ubuntu@24.04
sdks:
  - name: ros2-desktop
    channel: 24.04/stable
+ - name: project-nav2-sdk
```

Note the `project-` prefix to the SDK name.
This prefix tells Workshop that it is an in-project SDK
whose definition is local to the project.

From there, we can launch a new workshop or
refresh an existing one with respectively:

```console
$ workshop launch
"nav2-dev" launched
```

or:

```console
workshop refresh
```

We can then open a shell to the workshop:

```console
$ workshop shell
workshop@nav2-dev-967fc9ea:/project$
```

and verify that we can immediately start developing:

```console
$ colcon build
Starting >>> nav2_common
Starting >>> nav_2d_msgs
Starting >>> nav2_loopback_sim
...
Starting >>> nav2_system_tests
[Processing: nav2_system_tests]
Finished <<< nav2_system_tests [54.9s]

Summary: 43 packages finished [16min 10s]
```

## Adding Workshop actions

With our Nav2 workshop fully defined,
we can add 'actions' to it.
[Actions](https://ubuntu.com/workshop/docs/explanation/workshops/concepts/#actions)
are a convenient way to automatize mundane tasks,
and can show how a project is expected to be used.

Let us add a couple actions to the Nav2 workshop.
First, we add an action to build the project:

```diff
name: nav2-dev
base: ubuntu@24.04
sdks:
  - name: ros2-desktop
    channel: 24.04/stable
  - name: project-nav2-sdk
+
+actions:
+ build: colcon build --symlink-install --mixin release ccache lld "$@"
```

Here we define the action `build` that invokes Colcon
with a set of predefined flags.
The last parameter, `"$@"`,
forwards any user input to the command.

Since the Colcon flags of our action are not compatible with the previous Colcon run,
let's clean the build artifacts first:

```console
workshop exec colcon clean workspace -y
```

Calling an action happens outside the workshop environment,
i.e. without establishing a shell to it:

```console
$ workshop run nav2-dev build
Starting >>> nav2_common
Starting >>> nav_2d_msgs
Starting >>> nav2_loopback_sim
...
Starting >>> nav2_system_tests
[Processing: nav2_system_tests]
Finished <<< nav2_system_tests [54.9s]

Summary: 43 packages finished [16min 10s]
```

The Nav2 workspace built successfully.

We can also run the action providing some extra Colcon flags:

```console
$ workshop run nav2-dev build --packages-up-to costmap_queue
Starting >>> nav2_common
...
Finished <<< costmap_queue [6.48s]

Summary: 8 packages finished [3min 29s]
```

Furthermore, while the `build` action we defined is a single command,
we can define actions that contain an entire script.
To do so, we use the pipe symbol in the action definition:

```diff
...
actions:
  build: colcon build --symlink-install --mixin release ccache lld "$@"
+
+ test: |
+   colcon test "$@"
+   colcon test-result
```

## Mounting SSH

One last tweak before we part.
At the beginning of this tutorial we used the SSH Git remote to clone
the Nav2 repository.
This implies that to interact with said remote,
we need to have access to our SSH key.
However, they are not present in this workspace.

If we try to pull new content from the remote,
we hit an error:

```console
$ workshop shell
$ cd ~/workspace/src/navigation2
$ git pull
git@github.com: Permission denied (publickey).
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
```

Rather than copying our precious private key to the container,
we are going to use an interface that allows us to seamlessly forward our SSH key:
the `ssh-agent` interface.

To enable it,
we simply add the interface to the in-project SDK definition:

```diff
name: nav2-sdk
title: ROS 2 Navigation SDK
...
+plugs:
+ ssh-agent:
+   interface: ssh-agent
```

When launching a new workshop,
this new interface appears in the list of connections:

```console
$ workshop connections
Interface  Plug                        Slot               Notes
gpu        nav2/ros2-desktop:gpu               nav2/system:gpu    -
mount      nav2/ros2-desktop:ccache-cache      nav2/system:mount  -
mount      nav2/ros2-desktop:colcon-artefacts  nav2/system:mount  -
mount      nav2/ros2-desktop:ros-cache         nav2/system:mount  -
```

All we have to do is to connect it:

```console
workshop connect nav2/nav2-sdk:ssh-agent
```

and our SSH key is now forwarded inside the container:

```console
$ workshop shell
$ cd ~/workspace/src/navigation2
$ git pull
Already up to date.
```
