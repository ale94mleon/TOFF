#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import os, warnings, tempfile
from rdkit import Chem
from rdkit.Chem import AllChem
from openff.toolkit.typing.engines.smirnoff import ForceField
from openff.toolkit.topology import Molecule
from openmm.app import PDBFile
import parmed
from typing import List, Iterable


#This module was strongly inspired in https://github.com/aniketsh/OpenFF/blob/82a2b5803e36b72f3525e3b8631cf256fbd8e35a/openff_topology.py

def confgen(mol: Chem.rdchem.Mol):
    """Create a 3D model from a smiles and return a pdbqt string and, a mol if ``return_mol = True``.

    Parameters
    ----------
    smiles : Chem.rdchem.Mol
        A valid RDKit molecule.

    Returns
    -------
    Chem.rdchem.Mol
        A new instance of the input molecule with a conformation.
    """
    mol = Chem.AddHs(mol)
    AllChem.EmbedMolecule(mol)
    AllChem.MMFFOptimizeMolecule(mol)
    return mol

def get_rdkit_mol(input_path_mol:str, gen_conformer:bool = False):
    """Get a file with a definition of a molecule and return the corresponded RDKit molecule object

    Parameters
    ----------
    input_path_mol : str
        The path were the file molecule is. Only the foll, following extensions are valid:
        #. inchi (only the first line of the file will be considered and should be a valid InChi string)
        #. smi (only the first line of the file will be considered and should be a valid SMILES string)
        #. mol
        #. mol2
    gen_conformer : bool, by default False
        If True the :meth:`toff.utils.confgen` will be applied on the molecule in order to generate a conformation.
        For .smi and .inchi entrance :meth:`toff.utils.confgen` is always called.

    Returns
    -------
    Chem.rdchem.Mol
        The RDKit molecule object

    Raises
    ------
    NotImplementedError
        In case of an invalid extension.
    """

    extension = os.path.basename(input_path_mol).split('.')[-1]

    if extension == 'inchi':
        with open(input_path_mol, 'r') as f:
            mol = Chem.MolFromInchi(f.readline())
    elif extension == 'smi':
        with open(input_path_mol, 'r') as f:
            mol = Chem.MolFromSmiles(f.readline())
    elif extension == 'mol':
        mol = Chem.MolFromMolFile(input_path_mol)
    elif extension == 'mol2':
        mol = Chem.MolFromMol2File(input_path_mol)
    # elif extension == 'pdb':
    #     mol = Chem.MolFromPDBFile(input_path_mol)
    else:
        raise NotImplementedError(f"Only: *.inchi, *.smi, *.mol, *.mol2 are valid extensions. But *.{extension} was provided")
        # raise NotImplementedError(f"Only: *.inchi, *.smi, *.pdb, *.mol, *.mol2 are valid extensions. But *.{extension} was provided")

    mol = Chem.AddHs(mol)
    if extension in ['inchi', 'smi']:
        mol = confgen(mol)
    else:
        if gen_conformer: mol = confgen(mol)

    if not mol:
        warnings.warn("Molecule was not converted. Check the input")
    return mol

def topology_writer(ligand_structure:parmed.structure.Structure, ext_types:List[str] = None, overwrite = False, out_dir:str = '.') -> None:
    """A toff wrapper around the `save` method of :meth:`parmed.structure.Structure`

    Parameters
    ----------
    ligand_structure : parmed.structure.Structure
        _description_
    ext_types : List[str], optional
        Any extension from:
        'pdb', 'pqr', 'cif','pdbx',
        'parm7', 'prmtop', 'psf', 'top',
        'gro', 'mol2', '.mol3', 'crd',
        'rst7', 'inpcrd', 'restrt', 'ncrst'
        by default None which means that it will output: 'top', 'pdb', 'gro' files
    overwrite : bool, optional
        If True it will overwrite existing output files, by default False
    out_dir : str, optional
        Where the files will be written, by default '.'
    """

    valid_ext_types = [
                'pdb', 'pqr', 'cif','pdbx',
                'parm7', 'prmtop', 'psf', 'top',
                'gro', 'mol2', 'mol3', 'crd',
                'rst7', 'inpcrd', 'restrt', 'ncrst',
                ]
    if not ext_types:
        ext_types = ['top', 'pdb', 'gro']

    for ext_type in ext_types:
        ext_type = ext_type.lower()
        if ext_type in valid_ext_types:
            path = os.path.join(out_dir, f"{ligand_structure.atoms[0].residue.name}.{ext_type}")
            ligand_structure.save(path, overwrite = overwrite)
        else:
            warnings.warn(f"{ext_type} is not a valid extension type. Only: {valid_ext_types}")

def get_partial_charges(ligand_structure:parmed.structure.Structure):
    """get the partial charges from a :meth:`parmed.structure.Structure` object.

    Parameters
    ----------
    ligand_structure : parmed.structure.Structure
        Here is the Structure object were the partial charges will be obtained.

    Returns
    -------
    numpy.array
        A numpy array of partial charges
    """
    return np.array([atom.charge for atom in ligand_structure])

def set_partial_charges(ligand_structure:Chem.rdchem.Mol, partial_charges:Iterable):
    """Set new partial charges to a :meth:`parmed.structure.Structure` object

    Parameters
    ----------
    ligand_structure : Chem.rdchem.Mol
        Here is the Structure object were the partial charges will be set.
    partial_charges : Iterable
        New partial charges to set. Should have the same len as atoms in ligand_structure

    Returns
    -------
    Chem.rdchem.Mol
        The ligand_structure with the new set of partial charges.
    """
    for charge, atom in zip(partial_charges, ligand_structure):
        atom.charge = charge
    return ligand_structure

def charge_sanitizer(rdkit_mol:Chem.rdchem.Mol, ligand_structure:parmed.structure.Structure):
    """Check and correct (if needed) if the formal charge from the rdkit_mol is not the same as the sum of
    of the partial charges of the ligand_structure.

    Parameters
    ----------
    rdkit_mol : Chem.rdchem.Mol
        A rdkit mol representation of ligand_structure.
    ligand_structure : parmed.structure.Structure
        The Structure where the charges must be check.

    Returns
    -------
    parmed.structure.Structure
        ligand_structure with the corrected partial charges
    """
    # Get formal charge
    formal_charge = Chem.GetFormalCharge(rdkit_mol)
    
    # Round up the formal charge
    for atom in ligand_structure:
        atom.charge = round(atom.charge,3)
    
    partial_charges = get_partial_charges(ligand_structure)
    diff = round(partial_charges.sum() - formal_charge, 3)
    if diff:
        # distribute the remaining charge among all atoms
        print(f"Charges will be corrected: partial_charge - formal_charge = {diff}")
        quotient = diff / rdkit_mol.GetNumAtoms()
        new_partial_charges = (partial_charges - quotient).round(3)
        # Handling possible problems on float operations
        new_diff = round(new_partial_charges.sum() - formal_charge, 3)
        if new_diff:
            random_idx = np.random.choice(range(len(new_partial_charges)),1)[0]
            new_partial_charges[random_idx] -= new_diff
        
        # Set corrected charges on the ligand_structure
        ligand_structure = set_partial_charges(ligand_structure, new_partial_charges)
        print(f"After correction: partial_charge - formal_charge = {round(get_partial_charges(ligand_structure).sum() - formal_charge, 3)}.")
    # else:
    #     print("No charge correction needed.")
    return ligand_structure
           

class Parameterize:
    """This is the main class for the parameterization
    """

    def __init__(
            self,
            force_field_code:str = 'openff_unconstrained-2.0.0.offxml',
            ext_types:List[str] = None,
            hmr_factor:float = None,
            overwrite:bool = False,
            out_dir:str = '.',
            ) -> None:
        """This is the constructor of the class.

        Parameters
        ----------
        force_field_code : str, optional
            Any valid Open Force Field string representation.
            Visit the `GitHub repo <https://github.com/openforcefield/openff-forcefields>`__ for
            more information, by default 'openff_unconstrained-2.0.0.offxml'
        ext_types : List[str], optional
            Any extension from:
            'pdb', 'pqr', 'cif','pdbx',
            'parm7', 'prmtop', 'psf', 'top',
            'gro', 'mol2', '.mol3', 'crd',
            'rst7', 'inpcrd', 'restrt', 'ncrst'
            by default None which means that it will output: 'top', 'pdb', 'gro' files
        hmr_factor : float, optional
            This is a factor in which the mass of the hydrogen atoms
            will be increased using the mass of the linked heavy atoms.
            Useful to increases the integrating time step to 4 fs, by default None
        overwrite : bool, optional
            If True it will overwrite existing output files, by default False
        out_dir : str, optional
            Where the files will be written, by default '.'
        """

        self.force_field_code = force_field_code
        self.ext_types = ext_types
        self.hmr_factor = hmr_factor
        self.out_dir = os.path.abspath(out_dir)
        self.overwrite = overwrite
    
    def __repr__(self) -> str:
        ext_types_to_print = self.ext_types
        if not ext_types_to_print:
            ext_types_to_print = ['top', 'pdb', 'gro']
        ext_types_to_print = ' '.join(ext_types_to_print)
        return f"{self.__class__.__name__}(force_field_code = {self.force_field_code}, "\
            f"ext_types = [{ext_types_to_print}], hmr_factor = {self.hmr_factor}, "\
            f"overwrite = {self.overwrite}, out_dir = {self.out_dir})"
    
    def __call__(self,  input_mol, mol_resi_name:str = "MOL", gen_conformer:bool = False):
        """This class is callable. And this is its implementation.
        it will return the specified files (ext_types in __init__) in the directory out_dir.

        Parameters
        ----------
        input_mol : str, Chem.rdchem.Mol molecule
            Could be a path to any file compatible with :meth:`toff.utils.get_rdkit_mol`:
            (.inchi, .smi, .mol, .mol2)
            or any valid RDKit molecule
        mol_resi_name : str, optional
            The residue name that will have the ligand. It is recommended to use
            name no longer than 4 characters, by default "MOL"
        gen_conformer : bool, optional
            If True, a conformer will be generated for input_mol, by default False

        Raises
        ------
        Exception
            Non supported input_mol
        Exception
            Some exceptions occurred getting the topologies.
        """
        
        if isinstance(input_mol, Chem.rdchem.Mol):
            rdkit_mol = Chem.AddHs(input_mol)
            if gen_conformer: rdkit_mol = confgen(rdkit_mol)
        elif isinstance(input_mol, str):
            rdkit_mol = get_rdkit_mol(input_path_mol = input_mol, gen_conformer = gen_conformer)
        else:
            raise Exception(f'input_mol must be an instance of Chem.rdchem.Mol or str. But it is {type(input_mol)}')
        
        if len(mol_resi_name) > 4:
            warnings.warn(f"mol_resi_name = {mol_resi_name} is to large. consider to use a code with no more than 4 characters.")

        # Create if needed the output directory
        if not os.path.isdir(self.out_dir): os.makedirs(self.out_dir)
        
        # Create temporal pdb file
        tmp_pdb = tempfile.NamedTemporaryFile(suffix='.pdb')
        Chem.MolToPDBFile(rdkit_mol, tmp_pdb.name)
        
        # Generate the topology
        try:
            openff_mol = Molecule(rdkit_mol)
            ligand_pdbfile = PDBFile(tmp_pdb.name)
            ligand_system = ForceField(self.force_field_code).create_openmm_system(openff_mol.to_topology())
            ligand_structure = parmed.openmm.load_topology(ligand_pdbfile.topology, ligand_system, xyz = ligand_pdbfile.positions)
        except Exception as e:
            raise Exception(e)

        # Make Hydrogens Heavy for 4fs timestep
        if self.hmr_factor:
            parmed.tools.HMassRepartition(ligand_structure, self.hmr_factor).execute()

        # Change the residue name, dafault MOL
        for atom in ligand_structure.atoms:
            atom.residue.name = mol_resi_name

        # Correct charges if needed
        ligand_structure = charge_sanitizer(rdkit_mol = rdkit_mol, ligand_structure = ligand_structure)
        
        # Write the output topologies
        topology_writer(
            ligand_structure = ligand_structure,
            ext_types = self.ext_types,
            out_dir = self.out_dir,
            overwrite = self.overwrite,
        )


if __name__ == '__main__':
    pass
