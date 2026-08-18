(tutorials-observability-deploy-cos-for-robotics-server-in-the-cloud)=

# Deploy {{ COS_ROB }} server in the cloud

```{warning}
**Beta Notice**: {{COS_ROB}} is currently in `beta`.
Content and features may change,
and some functionality may be incomplete or experimental.
Feedback is welcome as we continue to improve.
```

## Introduction

In this tutorial,
we will walk through the process of deploying the
**Canonical Observability Stack (COS) for robotics** on a cloud-based server.
By the end of this tutorial,
you will have a fully functional observability stack tailored for robotics,
enabling you to monitor ROS devices efficiently.

{{ COS_ROB }} is a lightweight,
highly integrated observability stack designed to run on Kubernetes,
offering a plug and play observability solution tailored for
monitoring robotics devices.
The server infrastructure integrates robotics-specific applications with
the ones provided by [COS-lite](https://charmhub.io/topics/canonical-observability-stack/editions/lite).
Moreover, it is designed with customization in mind.
It offers the flexibility to add new applications in the form of charms or
Open Container Initiative (`OCI`) images and enhance existing ones.

```{note}
The server side is designed for the Edge and capable of running alongside `MicroK8s`
and Juju with limited computing resources (around 8 GB of memory).
```

On the **server side**, {{ COS_ROB }} runs a suite of observability tools that
collect and process data from connected devices.
On the **device side**,
lightweight agents (packaged as **Snaps**) simplify device registration and
enable real-time monitoring.
This allows you to connect each robot in your fleet to the observability stack and
immediately start collecting insights.

Each robot in your fleet can be set up with the snap agents,
registered and observed,
allowing for efficient management across an entire fleet.

![image](https://assets.ubuntu.com/v1/64dae60b-cos-for-robotics.png)

## What you will learn

By following this tutorial, you will:

- Deploy {{ COS_ROB }} on a cloud-based Kubernetes environment
  using **Juju** and **`MicroK8s`**.
- Register a ROS 2 device with the server.
- Begin monitoring robotic devices using
  **Prometheus, Grafana, Loki, and Foxglove Studio**.
- Understand how {{ COS_ROB }} can be customized with
  additional applications and integrations.

---

## Server side

The **{{ COS_ROB }}** is a Juju-based observability stack
running on **Kubernetes**.
It includes the following key components:

- [`Foxglove Studio`](https://charmhub.io/foxglove-studio-k8s)
  – A visualization tool for robotics data.
- [`COS-registration-server`](https://charmhub.io/cos-registration-server-k8s)
  – Manages device registration.
- [`Prometheus`](https://charmhub.io/prometheus-k8s)
  – Collects and stores metrics.
- [`Loki`](https://charmhub.io/loki-k8s)
  – Handles logging for robotics devices.
- [`Alert Manager`](https://charmhub.io/alertmanager-k8s)
  – Manages alerts and notifications.
- [`Blackbox exporter`](https://charmhub.io/blackbox-exporter-k8s)
  – Blackbox probing of endpoints.
- [`Grafana`](https://charmhub.io/grafana-k8s)
  – Provides dashboards for visualization.

These components are at core of the stack and can be enhanced
with additional functionalities and applications.

In the next section, we will go step by step through the deployment process.

### Install prerequisites

```{important}
To follow this tutorial, you will need a machine or a VM with at least 8 GB of memory, 4 CPUs and 50 GB of storage.
A container won't be sufficient.
```

Let’s proceed with the installation.

#### 1. Install `MicroK8s`

Install the `microk8s` snap with:

```bash
sudo snap install microk8s --channel 1.35-strict
```

Add the user to the `microk8s` group for unprivileged access and
give use permission to read the `~/.kube` director:

```bash
sudo adduser $USER snap_microk8s
sudo chown -f -R $USER ~/.kube
```

Wait for `microk8s` to finish initializing with:

```bash
sudo microk8s status --wait-ready
```

Enable the storage and `dns` `addons` which are required for the Juju controller:

```bash
sudo microk8s enable hostpath-storage dns
```

Finally, ensure your new group membership is apparent in the current terminal
(not required once you have logged out and back in again):

```bash
newgrp snap_microk8s
```

#### 2. Install Juju

Install the Juju snap with:

```bash
sudo snap install juju --channel 3.6/stable
```

Since the Juju package is strictly confined, you also need to manually create a path:

```bash
mkdir -p ~/.local/share
```

Now bootstrap a Juju controller into your `MicroK8s`

```bash
juju bootstrap microk8s cos-robotics-controller
```

If successful the terminal will show the following message:

```console
Bootstrap complete, controller "cos-robotics-controller" is now available in namespace "controller-cos-robotics-controller"
```

#### 3. Configure and enable `Metallb`

The bundle comes with `Traefik` to provide ingress,
for which the `metallb` add-on must be enabled.
[`Metallb`](https://metallb.universe.tf/) provides load balancer functionality and
requires the source IP address of the host system for outbound connections.
Run the following command to retrieve the IP address:

```bash
sudo apt update && sudo apt install -y jq
IPADDR=$(ip -4 -j route get 2.2.2.2 | jq -r '.[] | .prefsrc')
```

Then, enable `metallb` with the following command:

```bash
sudo microk8s enable metallb:$IPADDR-$IPADDR
```

### Deploy the {{ COS_ROB }} bundle

The stack deployment relies on the infrastructure as code (IAC) tool
[Terraform](https://developer.hashicorp.com/terraform).
It allows to easily set up complex infrastructure from a YAML based recipe,
allowing for simplicity, re-usability & repeatability among (many) other things.

You can install Terraform from the [Store](https://snapcraft.io/terraform) with:

```console
sudo snap install terraform --classic
```

First, let us retrieve the Terraform plan:

```console
git clone --branch track/0 https://github.com/canonical/rob-cos-overlay.git
cd rob-cos-overlay/terraform/rob-cos
```

Then we have to initialize the project:

```console
terraform init
```

In order to deploy {{ COS_ROB }},
we create a dedicated model with the following:

```bash
juju add-model cos-robotics-model
juju switch cos-robotics-model
```

Finally, deploy it with:

```bash
terraform apply -var="model=cos-robotics-model"
```

When prompted, type "yes" to confirm.
Now you can sit back and watch the deployment take place:

```bash
juju status --watch 5s --color --relations
```

COS will be ready to use when the `juju status` shows
all the machines active and the agents idle as follow:

![image](./juju-status.jpg)

Now {{ COS_ROB }} is good to go:
you can register devices to it to begin the monitoring!

### Verify the deployment

When all the charms are deployed,
you can head over to browse their built-in web user interfaces.
You can find out their addresses from the
[`show-proxied-endpoints`](https://charmhub.io/traefik-k8s/actions)
`Traefik` action.
In your terminal type:

```bash
juju run traefik/0 show-proxied-endpoints
```

The catalogue endpoint can be visualized on your browser and
it will list the catalogue of applications offered by {{ COS_ROB }}.
From the `proxied` endpoints, the catalogue URL should be similar to:

```{code-block} json
"catalogue":{"url": "http://<cos-robotics-server-ip>/cos-robotics-model-catalogue"}
```

Now by navigating to the catalogue URL in your browser,
the catalogue of all the available application will be displayed:

![image](./catalogue.jpg)

#### Grafana login

Clicking on the **Grafana** application will prompt you for
username and password as follows:

```{figure} https://assets.ubuntu.com/v1/bf1fa2db-grafana_welcome.png
   :alt: Grafana Dashboard

   Grafana login page
```

The default password for Grafana is automatically generated for every installation.
To access `Grafana's` web interface, use the username `admin`,
and the password obtained from the
[get-admin-password](https://charmhub.io/grafana-k8s/actions) action as follows:

```bash
juju run grafana/0 get-admin-password
```

---

## Next steps: device setup

Now that the server is set up,
let’s see how to deploy and register a device for monitoring.

> **Note**: The device setup is covered in a the next tutorial.
   You can find it at {ref}`tutorials-observability-deploy-cos-for-robotics-agent-on-your-robot`.
