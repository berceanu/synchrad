.. _building-karolina:

Karolina (IT4I)
===============

The `Karolina cluster <https://docs.it4i.cz/karolina/introduction/>`_ is located at `IT4I, Technical University of Ostrava <https://www.it4i.cz/en>`__.


Introduction
------------

If you are new to this system, **please see the following resources**:

* `IT4I user guide <https://docs.it4i.cz>`__
* Batch system: `PBS <https://docs.it4i.cz/general/job-submission-and-execution/>`__
* `Filesystems <https://docs.it4i.cz/karolina/storage/>`__:

  * ``$HOME``: per-user directory, use only for inputs, source and scripts; backed up (25GB default quota)
  * ``/scatch/``: `production directory <https://docs.it4i.cz/karolina/storage/#scratch-file-system>`__; very fast for parallel jobs (20TB default)


.. _building-karolina-preparation:

Preparation
-----------

Use the following commands to download the SynchRad source code:

.. code-block:: bash

   git clone https://github.com/berceanu/synchrad.git $HOME/src/synchrad
   
On Karolina, we recommend running on the accelerator nodes with fast A100 GPUs.

We use system software modules, add environment hints and further dependencies via the file ``$HOME/karolina_synchrad.profile``.
Create it now:

.. code-block:: bash

   cp $HOME/src/synchrad/Tools/machines/karolina-it4i/karolina_synchrad.profile.example $HOME/karolina_synchrad.profile

.. dropdown:: Script Details
   :color: light
   :icon: info
   :animate: fade-in-slide-down

   .. literalinclude:: ../../../../Tools/machines/karolina-it4i/karolina_synchrad.profile.example
      :language: bash
      :caption: ``$HOME/src/synchrad/Tools/machines/karolina-it4i/karolina_synchrad.profile.example``.

Edit the 2nd line of this script, which sets the ``export proj=""`` variable.
For example, if you are member of the project ``DD-23-83``, then run ``vi $HOME/karolina_synchrad.profile``.
Enter the edit mode by typing ``i`` and edit line 2 to read:

.. code-block:: bash

   export proj="DD-23-83"

Exit the ``vi`` editor with ``Esc`` and then type ``:wq`` (write & quit).

.. important::

   Now, and as the first step on future logins to Karolina, activate these environment settings:

   .. code-block:: bash

      source $HOME/karolina_synchrad.profile
   
   You can add the line above to your ``$HOME/.bashrc`` file.

Finally, since Karolina does not yet provide software modules for some of our dependencies, 
install them once, and activate the newly created ``Python`` virtual environment:

.. code-block:: bash

   bash $HOME/src/synchrad/Tools/machines/karolina-it4i/install_dependencies.sh
   source $HOME/sw/karolina/gpu/venvs/synchrad/bin/activate

.. dropdown:: Script Details
   :color: light
   :icon: info
   :animate: fade-in-slide-down

   .. literalinclude:: ../../../../Tools/machines/karolina-it4i/install_dependencies.sh
      :language: bash
      :caption: ``$HOME/src/synchrad/Tools/machines/karolina-it4i/install_dependencies.sh``.

Now, you can :ref:`submit Karolina compute jobs <running-karolina>` for SynchRad :ref:`Python (PICMI) scripts <usage-picmi>` (:ref:`example scripts <usage-examples>`).
Or, you can use the SynchRad executables to submit Karolina jobs (:ref:`example inputs <usage-examples>`).
For executables, you can reference their location in your :ref:`job script <running-karolina>` or copy them to a location in ``/scatch/``.


.. _building-karolina-update:

Update SynchRad & Dependencies
---------------------------

If you already installed SynchRad in the past and want to update it, start by getting the latest source code:

.. code-block:: bash

   cd $HOME/src/synchrad

   # read the output of this command - does it look ok?
   git status

   # get the latest SynchRad source code
   git fetch
   git pull

   # read the output of these commands - do they look ok?
   git status
   git log # press q to exit

And, if needed,

- :ref:`update the karolina_synchrad.profile file <building-karolina-preparation>`,
- log out and into the system, activate the now updated environment profile as usual,
- :ref:`execute the dependency install script <building-karolina-preparation>`.

As a last step, ... 


.. _running-karolina:

Running
-------

The batch script below can be used to run a SynchRad simulation on multiple GPU nodes (change ``#PBS -l select=`` accordingly) on the supercomputer Karolina at IT4I.
This partition as up to `72 nodes <https://docs.it4i.cz/karolina/hardware-overview/>`__.
Every node has 8x A100 (40GB) GPUs and 2x AMD EPYC 7763, 64-core, 2.45 GHz processors.

Replace descriptions between chevrons ``<>`` by relevant values, for instance ``<proj>`` could be ``DD-23-83``.
Note that we run one MPI rank per GPU.

.. dropdown:: Script Details
   :color: light
   :icon: info
   :animate: fade-in-slide-down

   .. literalinclude:: ../../../../Tools/machines/karolina-it4i/karolina_gpu.qsub
      :language: bash
      :caption: You can copy this file from ``$HOME/src/synchrad/Tools/machines/karolina-it4i/karolina_gpu.qsub``.

To run a simulation, copy the lines above to a file ``karolina_gpu.qsub`` and run

.. code-block:: bash

   qsub karolina_gpu.qsub

to submit the job.
