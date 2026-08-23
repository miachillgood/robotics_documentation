(how-to-guides-maintenance-enable-ros-esm)=

# Enable ROS ESM

ROS ESM builds on two Canonical ESM products: `ESM-infra` and `ESM-apps`.
As a result, there are three steps to enabling ROS ESM:

1. Obtaining your Ubuntu Pro token
2. Enabling ESM-infra and ESM-apps
3. Enabling ROS ESM.

Note that `ESM-infra` and `ESM-apps` are required dependencies of ROS ESM.

## Obtain your authentication token

Access to ESM is controlled by a token associated with
your Ubuntu Single Sign-on `(SSO)` account.
To obtain a token go to this page <https://ubuntu.com/pro/subscribe>.
You can register for free up to 5 tokens to try out Ubuntu Pro and ROS ESM.
If you already purchased ROS ESM or Ubuntu Pro,
then you will have the token and you can review it at:

<https://ubuntu.com/pro>

[Get in touch with us](https://ubuntu.com/robotics/ros-esm#get-in-touch)
if you need a personalised offer.

## Enable ESM-infra and ESM-apps

In order to enable these services, you will need:

- An Ubuntu LTS machine with a version similar to or above 16.04 LTS
- Sudo access
- An email address, or an existing Ubuntu One account
- Ubuntu Pro client version `27.11.2` or newer

Once you have your Ubuntu Pro token, make sure your Pro client is up to date:

`````{tabs}

````{tab}  Ubuntu 20.04 and later

```bash

sudo apt update && sudo apt upgrade
sudo apt install -y ubuntu-pro-client
```

This is because the `ubuntu-advantage-tools` package has been deprecated in favour of the `ubuntu-pro-client` package.

> See More: For more information, please visit [Ubuntu Pro Client Guide](https://ubuntu.com/pro/tutorial).

````

````{tab} Ubuntu 18.04 and below

```bash
sudo apt update && sudo apt upgrade
sudo apt install -y ubuntu-advantage-tools
```

````

`````

### Confirm your Ubuntu Pro client version

Regardless of your Ubuntu distribution,
make sure you are running the latest version of the Ubuntu Pro client.
To check it, run:

```bash
pro version
```

You should have a version greater than or equal to `27.11.2`.

### Attach the Pro client

Use the client to attach this machine to your contract using your token:

```bash
sudo pro attach YOUR_TOKEN
```

In order to see which Ubuntu Pro services are enabled you can run:

```bash
$ pro status
SERVICE          ENTITLED  STATUS       DESCRIPTION
anbox-cloud      yes       disabled     Scalable Android in the cloud
esm-apps         yes       enabled      Expanded Security Maintenance for Applications
esm-infra        yes       enabled      Expanded Security Maintenance for Infrastructure
fips             yes       disabled     NIST-certified FIPS crypto packages
fips-updates     yes       disabled     FIPS compliant crypto packages with stable security updates
livepatch        yes       enabled      Canonical Livepatch service
ros              yes       disabled     Security Updates for the Robot Operating System
usg              yes       disabled     Security compliance and audit tools
```

You should see some of the Ubuntu Pro services,
such as Expanded Security Maintenance for Infrastructure `(esm-infra)`
automatically enabled,
while others will remain disabled until you switch them on.

If it’s not, enter the following:

```bash
sudo pro enable esm-infra
```

Then, enable ESM Apps with:

```bash
sudo pro enable esm-apps
```

At any time, you can check how many deb packages are installed on your machine and
from which source using:

```bash
pro security-status
```

Congratulations, you now have ESM-infra and ESM-apps enabled!
Run an upgrade to install available security updates, if any:

```bash
sudo apt update
sudo apt upgrade
```

## Enable ROS ESM

ROS ESM is exposed in the Pro client similar to `ESM-infra` and
`ESM-app`s and is controlled by that same token.
However, ROS ESM is disabled by default and not listed in the common service list.
First, let’s make sure that the Pro client is up-to-date:

```bash
pro version
```

Should return version `27.11.2` or greater.

Then, let’s make sure that your token is entitled to enabling ROS ESM with:

```bash
pro status --all
```

You should now see the following ROS ESM services: `ros` and `ros-updates`.
Make sure that the `entitled` column displays a `yes` in front of these services.
If not, please reach out to customer service.

Now you have everything needed to enable ROS ESM.
There are two suites available:

- **ros**: only security-related updates for ROS-related software.
- **ros-updates**: security and non-security-related updates for ROS-related software.
  These are security updates and bug fixes.

**To enable the ROS security updates**, run the following command:

```bash
sudo pro enable ros
```

**To enable non-security updates**, run the following command:

```bash
sudo pro enable ros-updates
```

Note that if you enter directly:

```bash
sudo pro enable ros-updates
```

You will be prompted to enable the `ros` service first, as `ros-updates` depends on `ros`.

## Rosdep set up

ROS ESM provides its own distribution and `rosdep` files.
Let's make sure you install `rosdep` from ESM and re-initialise it as follows:

`````{tabs}

````{tab}  Noetic/Foxy (Python3)

```bash
sudo apt install python3-rosdep
sudo rm /etc/ros/rosdep/sources.list.d/20-default.list
sudo rosdep init
rosdep update
```
````

````{tab} Kinetic/Melodic (Python2)

```bash
sudo apt install python-rosdep
sudo rm /etc/ros/rosdep/sources.list.d/20-default.list
sudo rosdep init
rosdep update
```

````
`````
