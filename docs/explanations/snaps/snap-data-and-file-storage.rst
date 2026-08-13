.. _explanations-snaps-snap-data-and-file-storage-topic-guide:

Snap data and file storage
==========================

Environment variables are widely used across Linux to provide convenient access to system and application properties.
Both ``snapcraft`` and ``snapd`` consume, set, and pass-through specific environment variables to support building and running snaps.

Snap makes available certain environment variables to identify data and file storage location at run-time.

Snaps runs in a custom environment specifically made for them. Additionally, our snap is strictly confined and immutable.
As a result, they have dedicated locations where they can write data.
Data environment variables provide different locations for snaps to write data depending on the purpose and lifespan of those data.

+-------------------------------------------------------------------------------------------------------------------------------+-----------------------------+------------------------+------------------------------+-----------------------------+
|                                          Environment variable                                                                 | Data backed up over updates | Data kept over updates |     Accessible from host     | Accessible from other snaps |
+===============================================================================================================================+=============================+========================+==============================+=============================+
| ``SNAP_USER_DATA``                                                                                                            | Yes                         | No                     | Yes                          | No                          |
+-------------------------------------------------------------------------------------------------------------------------------+-----------------------------+------------------------+------------------------------+-----------------------------+
| ``SNAP_USER_COMMON``                                                                                                          | No                          | Yes                    | Yes                          | No                          |
+-------------------------------------------------------------------------------------------------------------------------------+-----------------------------+------------------------+------------------------------+-----------------------------+
| ``SNAP_DATA``                                                                                                                 | Yes                         | No                     | Read - Yes/Write - Root only | No                          |
+-------------------------------------------------------------------------------------------------------------------------------+-----------------------------+------------------------+------------------------------+-----------------------------+
| ``SNAP_COMMON``                                                                                                               | No                          | Yes                    | Read - Yes/Write - Root only | No                          |
+-------------------------------------------------------------------------------------------------------------------------------+-----------------------------+------------------------+------------------------------+-----------------------------+
| ``SNAP_REAL_HOME`` (`Requires additional` `HOME interface <https://snapcraft.io/docs/reference/interfaces/home-interface/>`_) | No                          | Yes                    | Yes                          | Yes                         |
+-------------------------------------------------------------------------------------------------------------------------------+-----------------------------+------------------------+------------------------------+-----------------------------+


All the following examples are assuming the snap hello-world revision 27.

Note that ``SNAP_USER_DATA``, ``SNAP_USER_COMMON`` depend on the user. When the user is ``ROOT`` (for daemons and command launched with sudo), ``$HOME`` correspond to ``/root``.

The following diagram shows the relationships and location of a filesystem.

There is a dedicated location for each installed snap for storing data and files.

.. image:: https://lh4.googleusercontent.com/3pVIb4k5KpWSXWIa7u3Gjy9nL86NA7no6onrl2ci96EKh97EnRPxyHWDdxmC5W_4sae-LkpT-440IQ41udjKRXKcyiS5E_o-utTxC-kpanfIpJTD1W31d4mSCz6wiIE8bcVbXtccfTxhSSBXpfx5ZX8
	:width: 624
	:height: 376


SNAP_USER_DATA
--------------

The ``SNAP_USER_DATA`` variables store the path to the directory for the user data of a snap. This directory is owned and writable by the current user.

All the content of this directory is backed-up and restored across updates and reverts. This also means that the data stored here won’t be available for the next update.

This variable is typically pointing to the host location:

.. code:: shell

	$HOME/snap/hello-world/27

Also corresponding to:

.. code:: shell

	$HOME/snap/hello-world/current


This directory can be accessed with read/write permissions by the user even outside the snap.

The typical use case of this variable would be:

* Log files
* Revision specific configuration files
* Temporary runtime created files
  

SNAP_USER_COMMON
----------------

The ``SNAP_USER_COMMON`` variable stores the path to the directory for the user data that are common across revisions of a snap. This directory is owned and writable by the user.

Unlike ``SNAP_USER_DATA`` this directory is not backed up and restored across snap refresh and revert operations.

This variable is typically pointing to the host location:

.. code:: shell

	$HOME/snap/hello-world/common

The typical use case of this variable would be:

* Revision specific configuration files
* Any file that we want to keep over the updates

Similarly, there is ``SNAP_DATA`` and ``SNAP_COMMON`` for system specific data and not user specific data. They are respectively pointing to ``/var/snap/hello-world/27`` and ``/var/snap/hello-world/common``.

The `snap documentation for environment variables <https://snapcraft.io/docs/environment-variables>`_ describes many more features that could be useful in other projects.
