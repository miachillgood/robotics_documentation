# Part 1 - exercise: Add additional application to the snap

``` {important}
This exercise requires having followed the
{ref}`Tutorial 1: Packaging our first ROS application as a snap <tutorials-snaps-core-packaging-ros-application-getting-started>`.
```

Let’s do a little exercise.
Right now, our talker-listener only has one application.
How about you add another one?
Having the ROS 2 topic tools inside our snap would be great for some introspection.

## Assignment

Modify the `snapcraft.yaml` file:

* Add a new app entry for ros2topic
* Add the corresponding dependencies

Build and install the new snap.

### Outcome

By the end of this exercise, you will have a new command available:

```ros2-talker-listener.ros2topic hz /chatter```

* Note that the ROS 2 topic tools are only going to work with message types
  that are included in the snap.

## Solution

```{dropdown} Click here for the solution

  - Add `ros2topic` as a `stage-package` to have it available at run time:

    ```diff
    parts:
      ros-demos:
        plugin: colcon
        source: https://github.com/ros2/demos.git
        source-branch: humble
        source-subdir: demo_nodes_cpp
    -   stage-packages: [ros-humble-ros2launch]
    +   stage-packages: [ros-humble-ros2launch, ros-humble-ros2topic]
    ```

    - We add our dependency (`ros-humble-ros2topic`) to the `stage-packages` list.
    `Stage-packages` are packages that are required to run the part.
    Here we decided to add our dependency to our already existing `ros-demos` part
    for simplicity.
    Alternatively, we could have created an additional empty part
    simply to add our `stage-packages` dependency.

  * Add an additional app:

    ```diff
    apps:
      ros2-talker-listener:
        command: opt/ros/humble/bin/ros2 launch talker-listener talker_listener.launch.py
        daemon: simple
        plugs: [network, network-bind]
        extensions: [ros2-humble]

    + ros2topic:
    +   command: opt/ros/humble/bin/ros2 topic
    +   plugs: [network, network-bind]
    +   extensions: [ros2-humble]
    ```

    - We added another application entry to our snap. We kept the plugs and extensions and simply exposed the `ros2 topic` command.

  * Build and install the new snap:

    ```bash
    snapcraft pack
    sudo snap install ros2-talker-listener_0.1_*.snap --dangerous
    ```

  * Make sure everything works:

    ```bash
    $ ros2-talker-listener.ros2topic hz /chatter
    average rate: 1.000 min: 0.999s max: 1.000s std dev: 0.00049s window: 3
    ```

```
