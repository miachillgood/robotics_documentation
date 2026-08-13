:sequential_nav: next

.. _tutorials-snaps-core-learning-roadmap:

From zero to hero: deploy a robot with snaps and Ubuntu Core
============================================================

.. Include start summary

This series of tutorials introduce you to using **snaps and Ubuntu Core
for deploying ROS-based robots**.

Starting from a fresh install, these guides
take you through an initial ROS 'Hello World' example, tackle
packaging of a complete robot using snaps, and the creation of a custom
Ubuntu Core image for that robot—all while
exploring design and distribution concerns.

.. Include stop summary

.. toctree::
   :hidden:
   :maxdepth: 1

   Part 1: Packaging our first ROS application as a snap <packaging-ros-application-as-snap>
   Part 2: Packaging complex robotics software with snaps <packaging-complex-robotics-software-with-snaps>
   Part 3: Distribute ROS applications with the Snap Store <distribute-ros-apps-with-snap-store>
   Part 4: Building ROS snaps with content sharing <building-ros-snaps-with-content-sharing>
   Part 5: Create an Ubuntu Core image for the TurtleBot3 <create-ubuntu-core-image-for-turtlebot3>


* :doc:`Part 1: Packaging our first ROS application as a snap <./packaging-ros-application-as-snap>`
   Learn to package an app as a snap. Across this tutorial,
   we will explore how to build snaps for a robotics application.
   Through different examples,
   we will cover the basics of snap creation for a ROS and ROS 2 application.
   By introducing the main concepts of a snap,
   we will see how to confine your robotics application and make it installable on dozens of Linux distributions.

* :doc:`Part 2: Packaging complex robotics software with snaps <./packaging-complex-robotics-software-with-snaps>`
   Learn to package a complete robot software stack as a snap.
   Across this tutorial,
   we will explore advanced snaps topics and tools that will show you how to structure,
   package, and test complex robotics applications.
   While covering the theoretical aspects of ROS snaps,
   we will apply all this knowledge to TurtleBot3 for a more interesting real-world scenario.

* :doc:`Part 3: Distribute ROS applications with the Snap Store <./distribute-ros-apps-with-snap-store>`
   Learn to distribute ROS applications to users or devices.
   Across this tutorial,
   we will explore the Snap Store to distribute robotics software and update like a global software vendor.

* :doc:`Part 4: Building ROS snaps with content sharing <./building-ros-snaps-with-content-sharing>`
   From the example shown in part 2 to exemplify one specific feature of snaps, content sharing.
   We will therefore revisit the entire example in order to make use of this feature.

* :doc:`Part 5: Create an Ubuntu Core image for the TurtleBot3 <./create-ubuntu-core-image-for-turtlebot3>`
   From the example shown in part 2 we will learn to build a custom Ubuntu Core image for the TurtleBot3.
   We will go through all the steps to create a custom Ubuntu image from the snaps we've developed.


See Also
--------

* `Snap - Tutorials <https://snapcraft.io/docs/snap-tutorials>`_
   This section of documentation contains step-by-step tutorials to help outline what
   snap is capable of while helping you achieve specific aims,
   such as installing your favourite applications, taking a data snapshot, removing snaps.

* `Snapcraft - Tutorials <https://documentation.ubuntu.com/snapcraft/stable/tutorials/>`_
   This section of documentation contains step-by-step tutorials to help us learn
   how to build snap packages of our applications and services,
   for desktop, servers and embedded devices.

* `Ubuntu core - Tutorials <https://ubuntu.com/core/docs/tutorials>`_
   This section of documentation contains step-by-step tutorials to help outline
   what Ubuntu Core is capable of while helping you achieve specific aims,
   such as installing Ubuntu Core or building a custom image for your device.
