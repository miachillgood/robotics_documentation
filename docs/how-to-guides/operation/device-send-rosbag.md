(how-to-guides-operation-device-send-rosbag)=

# Send rosbags to {{ COS_ROB }}

In this how-to,
we detail how to set up and configure a robot to send
rosbags to the {{ COS_ROB }} server.

We thus assume that a {{ COS_ROB }} server is up and running.
You may refer to the tutorial
{ref}`Deploy {{ COS_ROB }} server in the cloud <tutorials-observability-deploy-cos-for-robotics-server-in-the-cloud>`.
to do so.

In addition, a cloud storage must be deployed and integrated with {{ COS_ROB }}.
Pick the tab below corresponding to the storage solution you deployed.

The following assumes that a file server
is deployed and integrated with {{ COS_ROB }}.
You may refer to the how-to
{ref}`Deploy a file server for {{ COS_ROB }} <how-to-guides-operation-deploy-caddy>`.
to do so.

## Setting up the agent

With the server side ready to receive rosbags,
we shall now set up the device side.

The setup is as simple as installing the snap on the robot:

```console
sudo snap install ros2-exporter-agent --channel=latest/beta
```

Once installed, we shall verify that its interfaces are connected:

```console
$ snap connections ros2-exporter-agent
Interface     Plug                                     Slot                                           Notes
content       ros2-exporter-agent:configuration-read   rob-cos-demo-configuration:configuration-read  -
content       ros2-exporter-agent:rob-cos-common-read  rob-cos-data-sharing:rob-cos-common-read       -
```

and that its services have automatically started:

```console
$ snap services ros2-exporter-agent
Service                                 Startup   Current   Notes
ros2-exporter-agent.auto-clean          enabled   active    timer-activated
ros2-exporter-agent.daily-rotation      enabled   active    timer-activated
ros2-exporter-agent.read-configuration  enabled   active    -
ros2-exporter-agent.recorder            enabled   active    -
ros2-exporter-agent.synchronization     enabled   active    timer-activated
```

In case the interfaces are not connected,
or if you are using your own configuration snap,
you can connect them with:

```console
sudo snap connect ros2-exporter-agent:rob-cos-common-read <my-data-sharing>:rob-cos-common-read
```

And:

```console
sudo snap connect ros2-exporter-agent:configuration-read <my-demo-configuration>:configuration-read
```

Once both interfaces are connected,
the exporter agent will automatically start recording rosbags and
send them to the file server on {{ COS_ROB }}.

They can be start/stop with their respective command:

```console
sudo snap stop ros2-exporter-agent.recorder
```

and:

```console
sudo snap stop ros2-exporter-agent.synchronization
```
