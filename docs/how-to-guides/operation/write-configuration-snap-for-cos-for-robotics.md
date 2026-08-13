(how-tos-operation-snap-configuration-for-cos)=

# Write a configuration snap for {{ COS_ROB }}

```{warning}
**Beta Notice**: {{COS_ROB}} is currently in `beta`.
Content and features may change,
and some functionality may be incomplete or experimental.
Feedback is welcome as we continue to improve.
```

{{ COS_ROB }} is composed of various snaps.
These snaps must be configured for your robots,
your needs and your setup.

In this how-to guide,
you will learn the different steps to define your applications configuration
and how to deploy them all in one snap.

This way all your {{ COS_ROB }} snap services are configured with one snap.

For the rest of the guide,
the presented configuration has been inspired from
[`rob-cos-demo-configuration`](https://github.com/canonical/rob-cos-demo-configuration/tree/main/snap/local/configuration).

## The configuration in {{ COS_ROB }}

For {{ COS_ROB }} snaps, the configuration is done by sharing files with a
[`content` interface](https://snapcraft.io/docs/reference/interfaces/content-interface/).

In this how-to,
you will deploy all configurations in one snap and share them with one interface.
This way the various snaps will pick the configurations they need.

### Snaps to configure

Before starting, let's present the snaps that are using the content interface:

#### [`cos-registration-agent`](https://snapcraft.io/cos-registration-agent)

The snap expects a `device.yaml` file to specify device specific information
to the server.
This file requires the UID of the device as well as the URL of the server.
Details about this file
[can be found on GitHub](https://github.com/canonical/cos-registration-agent?tab=readme-ov-file#config).

Additionally, the agent can upload application-specific data to the server:

- [Grafana dashboards](https://grafana.com/grafana/dashboards/)
- [Foxglove layouts](https://docs.foxglove.dev/docs/visualization/layouts)
- [Prometheus alerts rule files](https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/)
- [Loki alerts rule files](https://grafana.com/docs/loki/latest/alert/)

#### [`rob-cos-grafana-agent`](https://snapcraft.io/rob-cos-grafana-agent)

This snap is wrapping the [`grafana-agent`](https://grafana.com/docs/agent/latest/)
in [flow mode](https://grafana.com/docs/agent/latest/flow/), hence
a single [`river`](https://grafana.com/docs/agent/latest/flow/concepts/config-language/)
file is necessary under the name `grafana-agent.river`.

#### [`ros2-exporter-agent`](https://snapcraft.io/ros2-exporter-agent)

This snap expects a `ros2-data-exporter.yaml` file to
specify the ros2bags recording configurations.
The YAML file is a one to one match from the
[snap parameters available](https://github.com/canonical/ros2-exporter-agent/?tab=readme-ov-file#snap-parameters).

#### [`foxglove-bridge`](https://snapcraft.io/foxglove-bridge)

This snap expects a `foxglove-bridge.yaml` file to specify the bridge configurations.
The YAML file is a one to one match from the [`foxglove-bridge` configuration](https://github.com/foxglove/ros-foxglove-bridge?tab=readme-ov-file#configuration).

### The content sharing interface

In order to have a match between what the different snaps are expecting and
your configurations,
you must follow the format from the content sharing interface.

Expose a content interface [slot](https://snapcraft.io/docs/explanation/interfaces/all-about-interfaces/)
with all the configuration placed at the root of the slot's content, as shown below:

```YAML
slots:
  configuration-read:
    interface: content
    read:
      - path/to/configurations
```

#### Configuration files layout

Once the configuration is accessible to a snap,
the various services are expecting the configuration files in specific locations.

All the configuration files are relative to the root of the configuration.

##### `cos-registration-agent`

```BASH
.
├── device.yaml
├── foxglove_layouts
│   ├── layout1.json
│   └── layout2.json
├── grafana_dashboards
│   ├── dashboard1.json
│   └── dashboard1.json
├── loki_alert_rules
│   ├── alert1.rules
│   └── alert2.rules
└── prometheus_alert_rules
    ├── alert1.rules
    └── alert2.rules
```

##### `rob-cos-grafana-agent`

```BASH
.
└──  grafana-agent.river
```

##### `ros2-exporter-agent`

```BASH
.
└──  ros2-data-exporter.yaml
```

##### `foxglove-bridge`

```BASH
.
└──  foxglove-bridge.yaml
```

## Write the snap

Now, with a clear view of the content interface as well as the various configurations,
you can start creating the snap.

### Define the `snapcraft.yaml`

In a new directory,
start by creating a `snapcraft.yaml` with the following content:

```YAML
name: my-rob-cos-configuration
base: core24
version: git
summary: A snap for my custom configuration of the rob cos snaps.
description: |
  A snap for my configuration of the rob cos snaps on the device.

  This snap offers a custom configuration for a rob cos device.
  It also offers a content sharing interface, to allow snaps on a device that is meant
  to work with the rob cos ecosystem to easily get configured.

  It offers a slot called configuration-read that allows plugged snaps to read data
  stored in $SNAP/etc/configuration.

  Usage:

  Connect as follows:
  sudo snap connect rob-cos-snap:configuration-read my-rob-cos-configuration:configuration-read

grade: stable
confinement: strict
```

### Add the configurations to the snap

Under the folder `snap/local/configuration`, add all the configuration files.

Next, append the following part to your `snapcraft.yaml`:

```YAML
parts:
  configuration:
    plugin: dump
    source: snap/local/configuration/
    organize:
      '*': /etc/configuration/
```

The configurations files will now be added to your snap.

### Expose the configuration with the content interface

Expose the configurations shipped in the snap by adding the content interface.

To do so, add the following to your `snapcraft.yaml`:

```YAML
slots:
  configuration-read:
    interface: content
    read:
      - $SNAP/etc/configuration
```

### Use the configuration snap

Before using the configuration snap, build and install it:

```BASH
snapcraft pack
snap install my-rob-cos-configuration*.snap --dangerous
```

It can now be connected to the various applications you want to configure.
As an example, connect it to the `cos-registration-agent` with:

```bash
snap connect cos-registration-agent:configuration-read my-rob-cos-configuration:configuration-read
```

This connection will automatically trigger the
registration on the `cos-registration-agent` side.

You can apply the same connections to all the snaps.

Additionally,
you could add more features to your configuration snap to make it smarter.

A complete example of such snap can be found on GitHub:
[github.com/canonical/rob-cos-demo-configuration](https://github.com/canonical/rob-cos-demo-configuration/tree/main).

You can also find a collection of example configurations for the various
{{ COS_ROB }} server applications on GitHub:
[github.com/canonical/ROB-COS-configurations](https://github.com/canonical/ROB-COS-configurations/).
