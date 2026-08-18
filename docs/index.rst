.. _docs-index:

Robotics Documentation
======================

.. toctree::
  :hidden:
  :maxdepth: 3

  tutorials/index
  how-to-guides/index
  references/index
  explanations/index

**Ubuntu gives robotics teams a complete, production-grade platform** to package, deploy, and maintain robot software at scale.

**The Canonical Robotics stack is your end-to-end infrastructure, from first build to global fleet.** Ubuntu Core and Snaps give you a reliable, production-grade foundation for packaging and deploying ROS applications. COS for Robotics is your observability suite for monitoring robots in the field. And with ROS ESM, you get guaranteed security maintenance for your ROS environment, long after upstream end-of-life.

**Robotics developers shouldn't have to become DevOps engineers.** Our open source tools take this complexity off your plate, so you can focus on building great robots.

**The Canonical Robotics stack is for robotics developers and integrators** who need to ship robot applications reliably on solid open-source foundations.

In this documentation
=====================

* **First Steps:** :doc:`Canonical Robotics Stack overview <references/ref_architecture/reference_architecture>` 
* **Packaging & distribution:** :doc:`Package a ROS application as a snap <tutorials/snaps-core/packaging-ros-application-as-snap>` |  :doc:`ROS architectures with snaps <explanations/snaps/ros-architectures-with-snaps>` | :doc:`Deploy a robot with snaps and Ubuntu Core <tutorials/snaps-core/index>` | :doc:`Migrate from Docker to snap <how-to-guides/packaging/migrate_from_docker_to_snap>` | :doc:`Snapcraft plugins <references/snapcraft/plugins>` and :doc:`extensions <references/snapcraft/extensions>` for ROS
* **Observability & monitoring:** :doc:`Observability for robotics <explanations/observability/what-is-cos-for-robotics>` | :doc:`Monitor your robot fleet <tutorials/observability/index>` | :doc:`Alert rules configuration <explanations/observability/alert-rules-configuration-from-device>` | :doc:`Deploy COS with TLS encryption <how-to-guides/operation/deploy-cos-for-robotics-with-tls-encryption>`
* **Security & long term support:** :doc:`Harden your robot <how-to-guides/security/hardening-your-robot>` | :doc:`What is ESM for ROS <explanations/security/what-is-ros-esm>` | :doc:`Security vulnerability audits <explanations/security/security-audits>` | :doc:`Check if a CVE is fixed <how-to-guides/maintenance/check-cves>`

How this documentation is organized
-------------------------------------

.. list-table::
   :header-rows: 0
   :widths: 50 50

   * - `Tutorials <tutorials>`__

       .. include:: tutorials/index.md
          :start-after: % Include start summary
          :end-before: % Include stop summary

     - `How-to guides <how-to-guides>`__

       .. include:: how-to-guides/index.md
          :start-after: % Include start summary
          :end-before: % Include stop summary

   * - `Explanation <explanations>`__

       .. include:: explanations/index.md
          :start-after: % Include start summary
          :end-before: % Include stop summary

     - `Reference <references>`__

       .. include:: references/index.md
          :start-after: % Include start summary
          :end-before: % Include stop summary

Project and community
=====================

The Canonical Robotics stack is part of the Ubuntu ecosystem. Its products are open source projects that warmly welcome community contributions, suggestions, fixes and constructive feedback.

* `Our Code of Conduct <https://ubuntu.com/community/ethos/code-of-conduct>`_
* `Community engagement commitment <https://documentation.ubuntu.com/core/explanation/community-engagement/>`_
* `Join the Robotics conversation on Ubuntu Discourse <https://discourse.ubuntu.com/c/project/robotics/121>`_
* `Join the Snap(craft) forum <https://forum.snapcraft.io/c/device/10>`_
* `Interactive chat on Matrix.org <https://ubuntu.com/community/communications/matrix>`_

Thinking about using the Canonical Robotics stack for your next project? `Get in touch! <https://ubuntu.com/robotics#get-in-touch>`_

.. _heading--navigation:






..    .. list-table::
..       :header-rows: 1

..       * - Old path
..         - New URL
