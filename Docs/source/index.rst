:orphan:

Synchrotron Radiation calculator via openCL
-------------------------------------------

This tool computes the energy density of synchrotron radiation in the spectral volume using the Fourier transformed Lienard-Wiechert potentials (see eq. (14.65) of J.D.Jackson's *Classical electrodynamics*).

It processes the 3D (*x*, *y*, *z*, *px*, *py*, *pz*) trajectories of the charged point-like particles with *weights*, and maps the emitted energy to the 3D spectral domain (*omega*, *theta*, *phi*). 
The package also contains several convenience methods for pre- and post-processing.

Language and hardware
^^^^^^^^^^^^^^^^^^^^^

**SynchRad** is written in `openCL <https://www.khronos.org/opencl>`_ and is interfaced with Python via `PyOpenCL <https://mathema.tician.de/software/pyopencl>`_. 

The code also utilizes the `Mako <https://github.com/sqlalchemy/mako>`_ template manager for adjustments to data types and *native* functions. It has been tested on GPU and CPU devices using NVIDIA, AMD, and Apple platforms. 
It demonstrates robust performance on GPUs, while the `OpenMP implementation <https://github.com/hightower8083/chimera>`_ offers significant speed on CPUs.

Local install
^^^^^^^^^^^^^

Once **openCL** and **PyOpenCL** are installed (e.g., via `conda` or `pip`) and configured on your machine, **SynchRad** can be installed by cloning the source and executing the `setup.py` script::

   git clone https://github.com/hightower8083/synchrad.git
   cd synchrad/
   python setup.py install

For multi-GPU or CPU device usage through MPI, `mpi4py` is also required. To output results in VTK format via the `exportToVTK` method, the `tvtk.api` should be installed.

Usage
^^^^^

A sample usage of **SynchRad** is available in the `example/` folder of this repository.

For a more general use case, consider computing radiation from particles in a PIC simulation. If the PIC software outputs in the `OpenPMD standard <http://www.openpmd.org/#/start>`, the `openPMD-viewer <https://github.com/openPMD/openPMD-viewer>`_ can aid in conversion::

   from openpmd_viewer import OpenPMDTimeSeries, ParticleTracker
   from synchrad.utils import tracksFromOPMD

   ts = LpaDiagnostics('./run/diags_track/hdf5/', check_all_files=False)
   ref_iteration = ts.iterations[-1]
   pt = ParticleTracker( ts, iteration=ref_iteration, 
                         preserve_particle_index=True)

   tracksFromOPMD( ts, pt, ref_iteration=ref_iteration, fname='tracks.h5')

For more detailed guidance, check the tutorial notebooks in `tutorials/`.

Author and Contributions
^^^^^^^^^^^^^^^^^^^^^^^^

This software was developed by Igor A Andriyash (igor.andriyash@gmail.com) and is still in its early development stages.

All contributions are welcome, whether for testing, benchmarking, optimization, or the addition of utility methods.


.. raw:: html

   <style>
   /* front page: hide chapter titles
    * needed for consistent HTML-PDF-EPUB chapters
    */
   section#installation {
       display:none;
   }
   </style>


Installation
------------
.. toctree::
   :caption: INSTALLATION
   :maxdepth: 1
   :hidden:

   install/hpc