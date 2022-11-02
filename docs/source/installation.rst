Installation
============

Requirements:

    * `Python 3.8+ <https://docs.python.org/3/>`_.
    * `RDKit <https://www.rdkit.org/docs/>`_.
    * `NumPy <https://numpy.org/>`_.
    * `OpenMM <http://docs.openmm.org/latest/userguide/>`_.
    * `OpenFF-toolkit <https://docs.openforcefield.org/projects/toolkit/en/latest/>`_.
    * `ParmEd <https://parmed.github.io/ParmEd/html/>`_.

.. note::

    If you have all dependencies already installed you could try with ``pip install TOFF`` directly.
    But if it is not the case or some version conflicts occurred, think about installed in a isolated environment
    as it will be show in brief.

Via pip (standard)
------------------

In this case you must have a correct installation of all dependencies listed in before. If you already have it, skip the creation of the conda environment and the conda dependencies installation:

Create conda environment and install conda dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. note::
    It is important to select the channel `conda-forge`. If not, some conflicts could appear during the creation of the environment (`see here <https://docs.openforcefield.org/projects/toolkit/en/latest/installation.html>`_).


.. code-block:: bash

    conda create -n TOFF
    conda activate TOFF

Then install the dependencies libraries:

.. code-block:: bash

    conda install -y -c conda-forge openff-toolkit openmm

..  In the future we will consider to use the python modules `vina on pypi <https://pypi.org/project/vina/>`_. Finally:

pip install
~~~~~~~~~~~

.. code-block:: bash

    # To get the last "stable" version (strongly recommended). This project is still in beta state.
    pip install TOFF

or:

.. code-block:: bash

    # To get the version on development (not recommended)
    pip install git+https://github.com/ale94mleon/TOFF.git@main