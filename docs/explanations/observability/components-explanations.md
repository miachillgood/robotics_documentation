# {{ COS_ROB }} components

```{warning}
**Beta Notice**: {{COS_ROB}} is currently in `beta`.
Content and features may change, and some functionality may be incomplete or experimental.
Feedback is welcome as we continue to improve.
```

The {{ COS_ROB }} is meant to monitor your devices.
This means that we have a server hosting all our applications and
devices sending data to our server.

The server side,
based on [COS Lite](https://charmhub.io/topics/canonical-observability-stack/editions/lite)
is relying on Juju to orchestrate and MicroK8s to scale your applications.
For the devices,
all the components are snaps and can run on an Ubuntu machine or in the OS for robotics
[Ubuntu Core](https://ubuntu.com/core/docs).

## Server components

The charmed operators that make up {{ COS_ROB }} are available
as the pre-configured {{ COS_ROB }} bundle.
{{ COS_ROB }} is made up of the following Juju charmed operators:

- [`cos-registration-server-k8s`](https://charmhub.io/cos-registration-server-k8s)
- [`foxglove-studio-k8s`](https://charmhub.io/foxglove-studio-k8s)
- [`ros2bag-fileserver-k8s`](https://charmhub.io/ros2bag-fileserver-k8s)

Additionally,
you can [package your own cloud application as a charm](https://canonical-charmcraft.readthedocs-hosted.com/en/stable/tutorial/)
and deploy it along {{ COS_ROB }}.

### `cos-registation-server-k8s`

The `cos-registration-server-k8s` operator is the first entry point for devices.
With this server, devices are going to register themselves and upload their configurations.
The `cos-registration-server-k8s` is then synching all the configurations to
the appropriate applications (Grafana, Prometheus, Loki, etc.).
Additionally, the operator offers a UI for the user to
retrieve devices and the corresponding visualization.

The `cos-registration-server-k8s` is a charm for the
[`cos-registration-server`](https://github.com/canonical/cos-registration-server)
working in complement with the
[`cos-registration-agent`](https://snapcraft.io/cos-registration-agent).

### `foxglove-studio-k8s`

The `foxglove-studio-k8s` operator is the charm of the former open-source version of
[Foxglove Studio](https://foxglove.dev/).
The charm is meant to work with the
[`foxglove-bridge` snap](https://snapcraft.io/foxglove-bridge).
The operator can be used to access live ROS data with the `foxglove-bridge` or
to load bag files from the `ros2bag-fileserver-k8s`.

### `ros2bag-fileserver-k8s`

The `ros2bag-fileserver-k8s` operator is used to store robotics data from devices.
Robots are pushing data over SSH.
The robotics data (ROS 2 bags),
can latter be accessed with the file-server
([Caddy](https://caddyserver.com/docs/caddyfile/directives/file_server))
exposed by the operator.
Additionally,
the file-server has a UI so you can access the files and their links to provide them
to other applications (i.e. Foxglove Studio file entry).
The charm is meant to work with the [`ros2-exporter-agent`](https://snapcraft.io/ros2-exporter-agent).

```{note}
If the space on your server is limited,
make sure to clear periodically the data stored by the `ros2bag-fileserver-k8s`.
```

## COS Lite components

{{ COS_ROB }} is extending COS Lite and thus include its applications:

- [`prometheus-k8s`](https://charmhub.io/prometheus-k8s)
- [`alertmanager-k8s`](https://charmhub.io/alertmanager-k8s)
- [`loki-k8s`](https://charmhub.io/loki-k8s)
- [`grafana-k8s`](https://charmhub.io/grafana-k8s)
- [`traefik-k8s`](https://charmhub.io/traefik-k8s)
- [`catalogue-k8s`](https://charmhub.io/catalogue-k8s)

```{note}
More information about the COS Lite components can be found in the
[COS Lite documentation](https://charmhub.io/topics/canonical-observability-stack/editions/lite).
```

## Devices components

The snaps that make up {{ COS_ROB }} are available on the Snap Store.
{{ COS_ROB }} is made up of the following snaps:

- [`cos-registration-agent`](https://snapcraft.io/cos-registration-agent)
- [`foxglove-bridge`](https://snapcraft.io/foxglove-bridge)
- [`ros2-exporter-agent`](https://snapcraft.io/ros2-exporter-agent)
- [`rob-cos-data-sharing`](https://snapcraft.io/rob-cos-data-sharing)
- [`rob-cos-grafana-agent`](https://snapcraft.io/rob-cos-grafana-agent)
- [`rob-cos-demo-configuration`](https://snapcraft.io/rob-cos-demo-configuration)

<!-- pyml disable-next-line line-length -->
Additionally, you can [package your own device application as a snap and deploy it along {{ COS_ROB }} snaps](/tutorials/snaps-core/index.rst).

### `cos-registration-agent`

The `cos-registration-agent` snap is the single component directly
talking to the `cos-registration-server`.
It’s making sure the device configuration is propagated to the server.
It's reading its configuration from the `rob-cos-demo-configuration`.
Additionally, it exposes some data to the `rob-cos-data-sharing`.

### `foxglove-bridge`

The `foxglove-bridge` snap is meant to directly communicate with the `foxglove-studio-k8s`.
The snap is packaging the official
[`ros-foxglove-bridge`](https://github.com/foxglove/ros-foxglove-bridge).
It is reading its configuration from the `rob-cos-demo-configuration`.

###  `ros2-exporter-agent`

The `ros2-exporter-agent` snap is recording ROS 2 bags and
sending them to the `ros2bag-fileserver-k8s`.
The snap takes care of recording bag,
sending them to the server and then clean old ROS bags.
It is reading its configuration from the `rob-cos-demo-configuration`.
Additionally, the snap reads credentials from the `rob-cos-data-sharing`.

### `rob-cos-data-sharing`

The `rob-cos-data-sharing` snap is an almost empty snap.
It is simply used to share data between different snaps,
from the `cos-registration-agent` to the `ros2-exporter-agent`.
The data currently shared with the `rob-cos-data-sharing` are:
a UID file as well as an SSH public and private key.

### `rob-cos-grafana-agent`

The `rob-cos-grafana-agent` snap is packaging the official
[`grafana-agent`](https://grafana.com/docs/agent/latest/).
The snap is used to send data from the system as well as
logs to different applications (Prometheus, Loki, etc.).
The `grafana-agent` is configured in [Flow mode](https://grafana.com/docs/agent/latest/flow/).
It reads its configuration from the `rob-cos-demo-configuration`.

### `rob-cos-demo-configuration`

The `rob-cos-demo-configuration` snap is an example snap providing
the configuration to all the {{ COS_ROB }} snaps.
The snap is meant to be used as a reference but
could be used to try {{ COS_ROB }} on your devices.
You can find details about how-to write your own configuration file in the documentation:
{ref}`Write configuration snap for {{ COS_ROB }} <how-tos-operation-snap-configuration-for-cos>`.
