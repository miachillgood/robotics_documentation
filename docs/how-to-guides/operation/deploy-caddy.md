(how-to-guides-operation-deploy-caddy)=

# Deploy a Caddy file server for {{ COS_ROB }}

```{warning}
**Beta Notice**: {{COS_ROB}} is currently in `beta`.
Content and features may change,
and some functionality may be incomplete or experimental.
Feedback is welcome as we continue to improve.
```

In this how-to,
we will deploy a simple Caddy file server
in the **Canonical Observability Stack (COS) for robotics**.
We therefore assume that a {{ COS_ROB }} stack is up and running.
You may refer to the tutorial
{ref}`Deploy {{ COS_ROB }} server in the cloud <tutorials-observability-deploy-cos-for-robotics-server-in-the-cloud>`.
to do so.

By the end of this guide,
We will have a cloud storage available in {{ COS_ROB }} so that devices
can push rosbags for later use.

## Deploy Caddy

To deploy Caddy, hit the following command:

```console
juju deploy ros2bag-fileserver-k8s --resource caddy-fileserver-image=ghcr.io/ubuntu-robotics/ros2bag-fileserver:dev --storage database:=10G --config ssh-port=2222 --channel=0/stable
```

Once deployed,
we can integrate the file storage with {{ COS_ROB }}:

```console
juju relate ros2bag-fileserver-k8s:ingress-tcp traefik:ingress-per-unit
juju relate ros2bag-fileserver-k8s:ingress-http traefik:ingress
juju relate ros2bag-fileserver-k8s:catalogue catalogue:catalogue
juju relate cos-registration-server:auth-devices-keys ros2bag-fileserver-k8s:auth-devices-keys
```

We can monitor the deployment, including the relations with:

```console
juju status --watch 5s --color --relations
```

Once everything is green,
the storage is ready to receive rosbags from the devices.

---

## Next steps: device setup

Now that the storage is set up,
let’s see how to configure a device to upload rosbags:
{ref}`Send rosbags to {{ COS_ROB }} <how-to-guides-operation-device-send-rosbag>`.
