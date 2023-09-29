Summary
=======

The idea
--------
**TOFF** will automatically give you the topology for your small molecule that you need for Molecular Dynamic Simulation.
Usually this task involves a lot of efforts making the QM calculations: get charges, fit dihedral potential,
see contribution of the hydration shell and more and more aspects. `Open Force Field <https://openforcefield.org/>`_ is
a very active initiative and a perfect tool to get rid of these problems. Their `force fields <https://github.com/openforcefield/openff-forcefields>`_
are constantly under update. These force fields use the SMIRKS Native Open Force Field (SMIRNOFF) format, which helps to reach a wide number of chemical
structures.

Since version `0.1.0`_ it is also possible to get GAFF and Espaloma force field parameters.

**TOFF** is python module but also have a friendly command line interface.
The main class to work with is :meth:`toff.utils.Parameterize`. Examples on how to use both interface: as a module and as a command line are found in the ``Tutorials`` section


Input data
----------

The only input needed is the definition of the molecule to parameterize. The molecule could be a valid RDKit molecule (``Chem.rdchem.Mol``) or any other extension accepted by
the function :meth:`toff.utils.get_rdkit_mol`. In case the command line is used, the inputs are specified through a configuration ``yaml`` file
(see this `YouTube video <https://www.youtube.com/watch?v=1uFVr15xDGg&list=PL6ebkIZFT4xXiVdpOeKR4o_sKLSY0aQf_&index=11>`_ to get use to yaml file anatomy).

