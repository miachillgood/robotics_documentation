(explanations-observability-security-considerations-for-cos)=

# Security considerations for {{ COS_ROB }}

```{warning}
**Beta Notice**: {{ COS_ROB }} is currently in `beta`.
Content and features may change,
and some functionality may be incomplete or experimental.
Feedback is welcome as we continue to improve.
```

This page outlines the security considerations
to keep in mind when operating {{ COS_ROB }},
particularly when TLS encryption is enabled.
Understanding these limitations and risks will help you
make informed decisions when planning and maintaining your deployment.

## Handle CA distribution carefully

The root CA certificate must be manually distributed to every device
and operator laptop, as shown in the
[Enable TLS encryption in {{ COS_ROB }}](../../how-to-guides/operation/deploy-cos-for-robotics-with-tls-encryption.md).
Take care to transfer the CA file over a secure channel,
verify its integrity before installing it,
and never skip certificate validation to work around distribution issues —
doing so defeats the purpose of TLS entirely.
In large fleets or organisations with many operators,
the overhead of maintaining this process securely is worth considering
when choosing a TLS provider.
Refer to the [Security with X.509 certificates](https://charmhub.io/topics/security-with-x-509-certificates)
topic on Charmhub for guidance.

## Protect access to the Juju TLS model

The CA private key managed by the `self-signed-certificates` charm
is the root of trust for the entire deployment.
Any operator with write access to the `tls` Juju model
can issue certificates that will be trusted by all registered devices.
Apply the principle of least privilege to Juju user permissions
and restrict access to the `tls` model to authorised operators only.

## Understand the scope of system-wide CA trust on devices

Installing the CA certificate into `/usr/local/share/ca-certificates/`
and running `update-ca-certificates` extends trust to **every process**
running on that device, not only the COS agents.
Any certificate signed by this CA will be accepted as valid by the entire OS.
This is the intended behaviour for this deployment,
but it means the CA private key must be kept secure.
If the CA is compromised, all devices that have installed it must be considered at risk.

## Device leaf certificates are not automatically renewed

The `self-signed-certificates` charm handles automatic renewal
of server-side certificates (Traefik, Grafana).
Device leaf certificates, however, are issued at registration time
and are not automatically renewed.
By default, device leaf certificates are valid for 90 days.
If a device leaf certificate expires,
the device will need to re-register with the server to obtain a new one.
Monitor certificate validity in long-running deployments,
and consider adjusting the default validity period to suit your fleet's operational cycle.

## There is no certificate revocation mechanism for devices

There is currently no certificate revocation list (CRL) or OCSP responder
for device leaf certificates.
If a device is decommissioned or suspected to be compromised,
be aware of the following limitations:

- The registration server is a configuration and listing service only.
  Removing a device from it does not prevent a compromised device
  from continuing to publish data, as there is no identity-based
  access control on data ingestion.
- If the device's private key may have been exposed,
  the only way to invalidate all issued certificates is to rotate the CA using the
  [`rotate-private-key`](https://charmhub.io/self-signed-certificates/actions) action
  on the `self-signed-certificates` charm.
  This requires reinstalling the new CA certificate on every device and operator laptop,
  and re-registering all devices.

## Device private key is protected by snap isolation, not encryption at rest

During registration, a private key and a CSR are generated on the device
and the private key is stored in the `rob-cos-data-sharing` snap data directory.
Snap data directories are owned by root and isolated between snaps
through AppArmor and seccomp policies,
which provides process-level protection.
Physical access to the device remains a risk:
consider enabling full-disk encryption on the robot's storage
when the threat model requires it.

## Foxglove bridge WebSocket is accessible on the local network

The Foxglove bridge listens for WSS (WebSocket over TLS) connections
using the device leaf certificate.
By default, this port may be reachable by any host on the local network.
Use firewall rules to restrict access to the Foxglove bridge port
to trusted hosts only.

## Ubuntu Core devices cannot use system-wide CA distribution

The `update-ca-certificates` mechanism used in this guide
works only on Ubuntu Desktop and Server.
Devices running Ubuntu Core do not support this system-wide approach yet,
and a suitable solution for Ubuntu Core is not yet available.
Take this into account when planning your fleet's operating system.
