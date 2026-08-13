# The `ros2-minimal` SDK

% Include start summary

The `ros2-minimal` SDK is used to set up a ROS 2 development environment.

In [Workshop](https://canonical-workshop.readthedocs-hosted.com/),
it sets up a bare minimum ROS 2 environment
and also attempts to install the project dependencies using Rosdep.
We detail hereafter what the `ros2-minimal` SDK contains and what does it configure.

% Include stop summary

It is available for the workshop bases:

- `22.04` on channel `humble/stable`
- `24.04` on channel `jazzy/stable`
- `26.04` on channel `lyrical/stable`

## How it works

The `ros2-minimal` SDK retrieves the ROS 2 GPG key from the Ubuntu key server and
sets up the ROS 2 repository.

It then installs the following packages:

- ros-dev-tools
- python3-colcon-argcomplete
- python3-colcon-alias
- python3-colcon-clean
- python3-colcon-mixin
- ros-${ROS_DISTRO}-ros-environment
- ros-${ROS_DISTRO}-ros-workspace
- ros-${ROS_DISTRO}-ament-index-cpp
- ros-${ROS_DISTRO}-ament-index-python
- ros-${ROS_DISTRO}-ros2run
- ros-${ROS_DISTRO}-ros2launch

And initializes Rosdep.

It then configures Colcon's auto-completion as well as its default
`~/.colcon/defaults.yaml` configuration file, and
retrieves and configures the default Colcon mixins.

The SDK sets up the ROS 2 workspace at `~/workspace/src` and
automatically sources the ROS 2 installation in `~/.profile`.

Last but not least,
it installs the project dependencies using `rosdep install`.

## Example

Please refer to the tutorial ['ROS 2 development using Workshop'](#tutorials-workshop-ros2-dev-getting-started)
for a complete example of using Workshop for ROS 2 development.
