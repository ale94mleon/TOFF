#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from small import Parameterize
import tempfile, os, yaml, subprocess
from rdkit import Chem

tmp_dir = tempfile.TemporaryDirectory().name
tmp_dir = 'topo'
valid_inputs = {
    'rdkit': Chem.MolFromSmiles('CC'),
    'smi': os.path.join(tmp_dir,'mol.smi'),
    'inchi': os.path.join(tmp_dir,'mol.inchi'),
    'mol': os.path.join(tmp_dir,'mol.mol'),
    # 'mol2': os.path.join(tmp_dir,'mol.mol2'),
    # 'pdb': os.path.join(tmp_dir,'mol.pdb'),
}

# Saving the molecules in different formats
with open(valid_inputs['smi'], 'w') as f: f.write(Chem.MolToSmiles(valid_inputs['rdkit']))
with open(valid_inputs['inchi'], 'w') as f: f.write(Chem.MolToInchi(valid_inputs['rdkit']))
Chem.MolToMolFile(valid_inputs['rdkit'], valid_inputs['mol'])
# Chem.MolToPDBFile(valid_inputs['rdkit'], valid_inputs['pdb'])

# Saving minimalist configuration file
config_yml = os.path.join(tmp_dir,'config.yml')
config_dict ={
    'input_mol': valid_inputs['mol'],
    'overwrite': True,
    'out_dir': tmp_dir,
    'gen_conformer': True,
    'hmr_factor': 3,
    'mol_resi_name': 'CMD'
}
with open(config_yml, 'w') as f:
    yaml.dump(config_dict,f)

def test_Parameterize():
    parameterizer = Parameterize(overwrite=True,out_dir=tmp_dir)
    for key in valid_inputs:
        print(key)
        parameterizer(input_mol=valid_inputs[key], mol_resi_name=key[:3], gen_conformer=True)

    # # test HMR
    # parameterizer = Parameterize(overwrite=True,out_dir=tmp_dir, hmr_factor=2.5)
    # parameterizer(input_mol=valid_inputs[key], mol_resi_name='HMR', gen_conformer=False)

def test_cmd_Parameterize():
    process = subprocess.run(f'parameterize {config_yml}', shell=True, executable='/bin/bash', stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    returncode = process.returncode
    if returncode != 0:
        raise RuntimeError(process.stderr)

if __name__ == '__main__':
    test_cmd_Parameterize()