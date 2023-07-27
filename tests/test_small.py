#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from toff import Parameterize
import tempfile, os, yaml
import subprocess # nosec
from rdkit import Chem
import pytest

tmp_dir = tempfile.TemporaryDirectory()

valid_inputs = {
    'rdkit': Chem.MolFromSmiles('CC'),
    'smi': os.path.join(tmp_dir.name,'mol.smi'),
    'inchi': os.path.join(tmp_dir.name,'mol.inchi'),
    'mol': os.path.join(tmp_dir.name,'mol.mol'),
    # 'mol2': os.path.join(tmp_dir.name,'mol.mol2'),
    # 'pdb': os.path.join(tmp_dir.name,'mol.pdb'),
}

# Saving the molecules in different formats
with open(valid_inputs['smi'], 'w') as f: f.write(Chem.MolToSmiles(valid_inputs['rdkit']))
with open(valid_inputs['inchi'], 'w') as f: f.write(Chem.MolToInchi(valid_inputs['rdkit']))
Chem.MolToMolFile(valid_inputs['rdkit'], valid_inputs['mol'])
# Chem.MolToPDBFile(valid_inputs['rdkit'], valid_inputs['pdb'])
print(os.listdir(tmp_dir.name))
# Saving minimalist configuration file
config_yml = os.path.join(tmp_dir.name,'config.yml')
config_dict ={
    'input_mol': valid_inputs['mol'],
    'overwrite': True,
    'out_dir': tmp_dir.name,
    'hmr_factor': 3,
    'mol_resi_name': 'CMD'
}
with open(config_yml, 'w') as f:
    yaml.dump(config_dict,f)


@pytest.mark.filterwarnings("ignore:pkg_resources is deprecated")
def test_Parameterize_openff():
    parameterizer = Parameterize(overwrite=True,out_dir=tmp_dir.name, force_field_type='openff')
    for key in valid_inputs:
        print(key)
        parameterizer(input_mol=valid_inputs[key], mol_resi_name=key[:3])

def test_Parameterize_gaff():
    parameterizer = Parameterize(overwrite=True,out_dir=tmp_dir.name, force_field_type = 'gaff')
    for key in valid_inputs:
        print(key)
        parameterizer(input_mol=valid_inputs[key], mol_resi_name=key[:3])

def test_Parameterize_espaloma():
    try:
        import espaloma
    except Exception:
        pytest.xfail("espaloma is not installed")
    parameterizer = Parameterize(overwrite=True,out_dir=tmp_dir.name, force_field_type = 'espaloma')
    for key in valid_inputs:
        print(key)
        parameterizer(input_mol=valid_inputs[key], mol_resi_name=key[:3])
    # # test HMR
    # parameterizer = Parameterize(overwrite=True,out_dir=tmp_dir, hmr_factor=2.5)
    # parameterizer(input_mol=valid_inputs[key], mol_resi_name='HMR')

def test_cmd_Parameterize():
    process = subprocess.run(
        f'parameterize {config_yml}',
        shell=True, executable='/bin/bash', stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, text=True
    ) # nosec
    returncode = process.returncode
    if returncode != 0:
        raise RuntimeError(process.stderr)


if __name__ == '__main__':
    pass