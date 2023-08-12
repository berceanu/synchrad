.. _install-hpc:

HPC
===

On selected high-performance computing (HPC) systems, SynchRad has documented or even pre-build installation routines.
Follow the guide here instead of the generic installation routines for optimal stability and best performance.


.. _install-hpc-profile:

synchrad.profile
-------------

Use a ``synchrad.profile`` file to set up your software environment without colliding with other software.
Ideally, store that file directly in your ``$HOME/`` and source it after connecting to the machine:

.. code-block:: bash

   source $HOME/synchrad.profile

We list example ``synchrad.profile`` files below, which can be used to set up SynchRad on various HPC systems.


.. _install-hpc-machines:

HPC Machines
------------

This section documents quick-start guides for a selection of supercomputers that SynchRad users are active on.

.. toctree::
   :maxdepth: 1

   hpc/karolina

.. tip::

   Your HPC system is not in the list?
   `Open an issue <https://github.com/hightower8083/synchrad/issues>`__ and together we can document it!