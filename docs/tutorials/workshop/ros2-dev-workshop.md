(tutorials-workshop-ros2-dev-getting-started)=

# Getting started with Workshop

[**Workshop**](https://ubuntu.com/workshop/docs/)
is a tool for defining and handling ephemeral development environments.

% Include start summary

In this tutorial,
we will see how one can spawn and manage virtual development environments
tailored for ROS 2 projects using
[**Workshop**](https://ubuntu.com/workshop/docs/).

% Include stop summary

## Set up Workshop

Workshop relies on [LXD 6.3+](https://canonical.com/lxd),
we should therefore make sure a proper version is installed.

To install it from scratch:

```console
sudo snap install --channel=6/stable lxd
lxd init --minimal
```

To refresh an existing installation:

```console
sudo snap refresh --channel=6/stable lxd
```

The second prerequisite is ZFS support.
You can quickly check for this using the command:

```console
modprobe --dry-run zfs
```

In case this fails, you may have to install ZFS.
The following should work on Ubuntu:

```console
sudo apt-get install zfs-dkms zfsutils-linux
```

With those prerequisites fulfilled,
we can install Workshop:

```console
sudo snap install workshop --classic
```

## Launch a ROS 2 workshop

We will use the
[ROS 2 demos](https://github.com/ros2/demos)
repository to serve as the ROS 2 project we are developing.

Let's start by cloning the repository locally:

```console
git clone https://github.com/ros2/demos.git --branch lyrical
```

We can then create a workshop definition for this project:

```console
cd demos
touch workshop.yaml
```

and fill it with:

```yaml
name: demos-lyrical-dev
base: ubuntu@26.04
sdks:
  - name: ros2-desktop
    channel: lyrical/stable
```

The `name` tag is, as one might expect, the name of the workshop,
while the `base` indicates that we are using an Ubuntu 26.04 image.
The `sdks` are the pre-configured development environments that we wish to set up
in the workshop.
Here,
we use a single SDK, `ros2`, at the version `26.04` which corresponds to ROS 2 Lyrical.
This SDK is responsible for setting up a ready-to-use
ROS 2 Lyrical development environment.

And that is what we are going to see right away.

Launch the workshop with the command:

```console
workshop launch
```

After some time, the command returns and the workshop is ready to use.
We can confirm that with:

```console
$ workshop list
Workshop           Status  Notes
demos-lyrical-dev  Ready   -
```

Before jumping in,
let us summarize what happens in the background.

After hitting `launch`, Workshop creates an LXD container from an Ubuntu 26.04 image.
Once the container is up, it installs the SDKs.
More specifically, the `ros2` SDK sets up the ROS 2 repository and
installs the bare minimum ROS 2 packages
for a functioning ROS 2 development environment (think Colcon, Rosdep, Ament etc).
It adds the command to source the ROS 2 environment to the user `.profile` file
so that it is immediately and automatically available.
Similarly, it configures Colcon and its auto-completion.
Finally, it installs the dependencies of our project (in this case, the demos)
using Rosdep so that we are immediately ready to develop.

You can find more details at the [Workshop documentation website](https://ubuntu.com/workshop/docs/reference/cli/workshop/#workshop-launch).

## Develop for ROS 2 using Workshop

With the workshop up and running,
we can open a shell inside it and verify that everything is indeed ready to go:

```console
$ workshop shell
workshop@demos-lyrical-dev-3b81c721:/project$ ls
CONTRIBUTING.md   composition            dummy_robot         lifecycle_py      pytest.ini
LICENSE           demo_nodes_cpp         image_tools         logging_demo      quality_of_service_demo
README.md         demo_nodes_cpp_native  intra_process_demo  pendulum_control  topic_monitor
action_tutorials  demo_nodes_py          lifecycle           pendulum_msgs     topic_statistics_demo
```

Upon entering the shell,
we find ourselves at the root directory of the demos project.
However, we see that it is mounted at `/project`.
For convenience, and to have a more familiar ROS 2 environment,
it is also linked at `~/workspace/src/demos`.
We can move there for the remainder of this tutorial:

```console
workshop@demos-lyrical-dev-3b81c721:/project$ cd ~/workspace/src/demos
workshop@demos-lyrical-dev-3b81c721:~/workspace/src/demos$
```

```{note}
While `/project` is the default path in workshop,
some of its commands, such as `exec`,
provide the flag `--cwd` to set the working directory in the workshop.
```

To make sure our environment is properly set up,
we can quickly check if the usual suspects are present:

```{note}
For readability,
we drop the `workshop@demos-lyrical-dev-3b81c721:~/workspace/src/demos` prefix
hereafter.
```

```console
$ which colcon
/usr/bin/colcon
$ which rosdep
/usr/bin/rosdep
$ ls /opt/ros/lyrical/
_local_setup_util.py  include         lib               local_setup.fish  local_setup.zsh  setup.bash  setup.sh   share
bin                   includefastcdr  local_setup.bash  local_setup.sh    opt              setup.fish  setup.zsh  tools
$ env | grep ROS
ROS_VERSION=2
ROS_PYTHON_VERSION=3
ROS_AUTOMATIC_DISCOVERY_RANGE=SUBNET
ROS_DISTRO=lyrical
```

As we can see, the ROS 2 Lyrical environment is installed and already sourced.

But can we really start developing right away?

```console
$ colcon build --packages-select demo_nodes_cpp --mixin debug
Starting >>> demo_nodes_cpp
[Processing: demo_nodes_cpp]
Finished <<< demo_nodes_cpp [46.8s]

Summary: 1 package finished [46.8s]
```

Well it seems so!

Colcon is installed and so are its default mixins.
It is also pre-configured to make use of the
`~/workspace/src/{build,install,log,src}` environment in its
`~/.colcon/defaults.yaml` configuration file.

## Connect VSCode to Workshop

Having a containerized ROS 2 development environment tailored to our project
is neat, but interacting with it through a shell may be inconvenient.
For those who would prefer the reassuring interface of VSCode over Vim,
don't worry, Workshop comes with VSCode integration!

As a pre-requisite,
we have to make sure that VSCode `remote-ssh` plugin is installed.
To install it,
have a look at
[the documentation](https://code.visualstudio.com/docs/remote/remote-overview)
or use the command:

```bash
code --install-extension ms-vscode-remote.remote-ssh
```

With the plugin installed,
we can now enable it on our workshop following the
[workshop documentation](https://ubuntu.com/workshop/docs/how-to/develop-with-workshops/connect-vscode/)
which is summarized hereafter.

First, we add a new SDK to our workshop definition:

```diff
name: demos-lyrical-dev
base: ubuntu@26.04
sdks:
  - name: ros2
    channel: lyrical/edge
+ - name: vscode-remote
+   channel: latest/stable
```

after which we refresh the workshop:

```console
workshop refresh
```

Once the refresh finished,
we can get a hint at what to do next with the command:

```console
$ workshop tasks

  ...
  VS Code → Open Remote Window → Connect to host → workshop@10.41.49.51
```

The hint tells us how to connect to the workshop from VSCode interface.
Alternatively we can also do it from the command line with:

```console
code --folder-uri vscode-remote://ssh-remote+workshop@10.41.49.51/home/workshop/workspace
```

Just remember to change the IP address to the suggested one.
