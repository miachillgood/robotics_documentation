(reference-snapcraft-faq-troubleshooting)=

# FAQ & Troubleshooting

This page reference ROS and ROS 2 snap  common questions and troubleshooting:

## Frequently Asked Questions

If you cannot find an answer to your question here,
feel free to ask it on [the ubuntu forum](https://discourse.ubuntu.com/c/project/robotics/121).

## I cannot snap my application. What should I check?

* Snapcraft uses the familiar ROS tools (`rosdep`/`catkin`/`colcon` etc).
Which means that your application must follow the ROS directives for proper packaging,
such as declaring all the necessary dependencies in the *`package.xml`* files or
the install rules in your *`CMakeFile.txt`*.

Make sure that these are in good order before attempting to create a snap.

* Use colcon-in-container to validate your workspace before snapping \
  If you're encountering persistent issues when snapping your ROS 2 application,
  especially related to missing dependencies or environment mismatches,
  we recommend trying [**colcon-in-container**](https://github.com/canonical/colcon-in-container/blob/main/README.md).
  This tool builds and tests your ROS workspace inside an ephemeral,
  isolated container with a clean ROS environment.

## Which base should I use (`core18`, `core20`, `core22` or `core24`)?

* You should use the base that corresponds to your ROS version. That is,
  * `core18` for ROS Melodic and ROS 2 Dashing.
  * `core20` for ROS Noetic and ROS 2 Foxy.
  * `core22` for ROS 2 Humble.
  * `core24` for ROS 2 Jazzy.

## For ROS 1, do I have to expose `roscore` from my snap?

* Exposing a `roslaunch` command from your snap will
  automatically launch a `roscore` if needed.
  The only reason to expose explicitly the `roscore` would be if
  you plan to start the `roscore` explicitly from your snap.

## Where should my *snapcraft.yaml* file live?

* Within the package:
  * In `core20` and above, the *snap/* directory should be located at
    the root of the package (next to your *package.xml* file)
  * In `core18` the snap/ directory should be located either
    one folder behind your package root or at the root of your workspace
* Outside the package:
  * Using a `rosinstall` file to download the sources.
  * Using a single git repository holding the sources.

## Can my snap save data on the host?

* The snap defines some [environment variables for data and file storage](#explanations-snaps-snap-data-and-file-storage-topic-guide)
  pointing to different locations that a snap can write to
  depending on the use case of your data.
* You can save data that are common across revisions of a snap.
  These directories **won’t be backed-up** and restored across revisions:
  * `$SNAP_COMMON`, typical value: `/var/snap/hello-world/common`. Owned by `root`
  * `$SNAP_USER_COMMON`, typical value: `/home/$USER/snap/hello-world/common`.
    Owned by `$USER`
* You can save data for a revision of a snap.
  This directory **is backed up** and restored across revisions:
  * `$SNAP_DATA`, typical value: `/var/snap/hello-world/27`. Owned by `root`
  * `$SNAP_USER_DATA`, typical value: `/home/$USER/snap/hello-world/27`.
    Owned by `$USER`
* Additionally, with the [`home` interface](https://snapcraft.io/docs/reference/interfaces/home-interface/),
  your snap could access the real `$HOME` of the user by accessing `$SNAP_REAL_HOME`.

## Troubleshooting

## The command(s) `rosrun` and/or `roslaunch` are not available in my snap

* If this happens,
  it means that your ROS project does not define a runtime dependency on
  either `rosrun` nor `roslaunch` anywhere.
  You can fix this by declaring the dependency in the appropriate ROS *package.xml* file.
  Another option is to list either (or both) ROS packages as `stage-packages` in
  your *snapcraft.yaml*.
  The ROS packages for `rosrun` and `roslaunch` are respectively:
  * `ros-${ROS-DISTRO}-rosbash`
  * `ros-${ROS-DISTRO}-roslaunch`.

<!-- pyml disable-num-lines 3 line-length -->

## With `core18` Catkin plugin creates an external link that prevents the security checks to pass

* Please see: [Catkin generating an external link](https://forum.snapcraft.io/t/store-unable-to-accept-contains-external-symlinks-to-sudo-service/23269).

## Missing `lapack` and/or `blas`

* Paths to the libraries `lapack` and `blas` are not included
  in the library path by default.
  Thus, it must be extended manually in your app.

  ```yaml
  environment:
    "LD_LIBRARY_PATH": "$LD_LIBRARY_PATH:$SNAP/usr/lib/$SNAPCRAFT_ARCH_TRIPLET/blas:$SNAP/usr/lib/$SNAPCRAFT_ARCH_TRIPLET/lapack"
  ```

<!-- pyml disable-num-lines 3 line-length -->

## Warning: *“This part is missing libraries that cannot be satisfied with any available stage-packages known to snapcraft”*

* Some libraries are build-time only dependencies,
  but are still reported as run-time dependencies by `snapcraft`.
  This warning is a false positive and will be fixed soon in snapcraft.
  For instance, when snapping `ros2-demo` you might encounter:

  ```bash
  This part is missing libraries that cannot be satisfied with any available stage-packages known to snapcraft:
  # false-positive, none of the following are necessary at run-time
  libnddsc.so
  libnddscore.so
  libnddscpp.so
  librosidl_typesupport_connext_c.so
  librosidl_typesupport_connext_cpp.so
  librticonnextmsgcpp.so
  ```

## Strictly confined ROS 2 snaps shows an access error regarding shared memory

If you see something similar to:

```bash
[RTPS_TRANSPORT_SHM Error] Failed to create segment 86bb3c83d0835208: Permission denied ->   Function compute_per_allocation_extra_size
[RTPS_MSG_OUT Error] Permission denied -> Function init
```

* ROS 2 communication library is trying to use the shared memory mechanism.
  Don’t worry, even if you see this error,
  the messages are going to be transmitted (just not through shared memory).
  If you want to use the shared memory of ROS 2 within snap,
  visit: [ROS 2 shared memory in snap](#how-to-guides-packaging-ros-2-shared-memory-in-snaps)

## At runtime, the snap shows an error similar to

```bash
[rospack] Unable to create temporary cache file /home/USER/.ros/.rospack_cache.VyyWPF: Permission denied
```

* By default `rospack` and `roslog` write to the `$HOME/.ros`.
  When strictly confined a snap which doesn’t have the [`home` interface](https://snapcraft.io/docs/reference/interfaces/home-interface/)
  cannot access the host `$HOME`.
  Also, even with the [`home` plug](https://snapcraft.io/docs/reference/interfaces/home-interface/)
  the snap cannot access to hidden directories (.directories)
  for security reasons (like .ssh).
  * To solve that,
    we can write ROS logs in the `$SNAP_USER_DATA` environment variable.
    We can do so by defining the ROS environment variable `ROS_HOME`.
    We can do so by adding to a snap app in the `snapcraft.yaml`:

    ```yaml
        [...]
        apps:
          myapp:
            environment:
              ROS_HOME: $SNAP_USER_DATA/ros
            command: [...]
    ```

  * The data will also be available from the host in:
    `~/snap/YOUR_SNAP_NAME/current/ros`.

## Calling `snapcraft` give the following error

```bash
Failed to install GPG key: unable to establish connection to key server 'keyserver.ubuntu.com'

Recommended resolution:
Verify any configured GPG keys.

Detailed information:
GPG key ID: C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654
GPG key server: keyserver.ubuntu.com
```

* If the problem is persistent, it’s most probably a DNS issue.
  * To verify if it’s a DNS issue,
    if the following command succeeds it’s most probably a DNS issue:
    `sudo -E apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654`
  * We can also verify that the port `11371` is not blocked or occupied.

## ROS snap with shared memory doesn't receive or send data on topic

* If you have properly followed the [ROS snap and shared memory how to guide](#how-to-guides-packaging-ros-2-shared-memory-in-snaps)
  but still have problems,
  make sure that the different processes publishing/subscribing ROS 2 data over
  shared memory are using the same `USER`.
  [FastDDS shared memory can generate communication problems](https://github.com/eProsima/Fast-DDS-docs/blob/master/docs/fastdds/transport/shared_memory/shared_memory.rst?plain=1#L71:L78)
  if access from different users.
* Keep in mind that snap services are running with the `root` user
  while CLI applications might use a less privileged user (i.e: `ubuntu`)
  causing the FastDDS shared memory communication problems.
