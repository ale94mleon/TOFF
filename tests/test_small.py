#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for small-molecule parameterization with the Python API and the CLI."""
import os
import shutil
import subprocess  # nosec B404 - only used to run TOFF's own CLI
import tempfile

import pytest
import yaml
from rdkit import Chem

from toff import Parameterize

tmp_dir = tempfile.TemporaryDirectory(dir=".", prefix="toff-test-")

valid_inputs = {
    'rdkit': Chem.MolFromSmiles('CC'),
    'smi': os.path.join(tmp_dir.name, 'mol.smi'),
    'inchi': os.path.join(tmp_dir.name, 'mol.inchi'),
    'mol': os.path.join(tmp_dir.name, 'mol.mol'),
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
config_yml = os.path.join(tmp_dir.name, 'config.yml')
config_dict = {
    'input_mol': valid_inputs['mol'],
    'overwrite': True,
    'out_dir': tmp_dir.name,
    'hmr_factor': 3,
    'mol_resi_name': 'CMD'
}
with open(config_yml, 'w') as f:
    yaml.dump(config_dict, f)


def test_Parameterize_openff():
    """Parameterize every supported input type with OpenFF."""
    parameterizer = Parameterize(overwrite=True, out_dir=tmp_dir.name, force_field_type='openff')
    for key in valid_inputs:
        print(key)
        parameterizer(input_mol=valid_inputs[key], mol_resi_name=key[:3])


def test_Parameterize_gaff():
    """Parameterize every supported input type with GAFF."""
    parameterizer = Parameterize(overwrite=True, out_dir=tmp_dir.name, force_field_type='gaff')
    for key in valid_inputs:
        print(key)
        parameterizer(input_mol=valid_inputs[key], mol_resi_name=key[:3])


@pytest.mark.filterwarnings("ignore::Warning")  # Adjust the warning type as needed
def test_Parameterize_espaloma():
    """Parameterize every supported input type with Espaloma (skipped if it is not installed)."""
    pytest.importorskip("espaloma", reason="espaloma is not installed")
    parameterizer = Parameterize(overwrite=True, out_dir=tmp_dir.name, force_field_type='espaloma')
    for key in valid_inputs:
        print(key)
        parameterizer(input_mol=valid_inputs[key], mol_resi_name=key[:3])


def test_Parameterize_hmr():
    """Parameterize with hydrogen mass repartitioning."""
    parameterizer = Parameterize(overwrite=True, out_dir=tmp_dir.name, hmr_factor=2.5)
    parameterizer(input_mol=valid_inputs["rdkit"], mol_resi_name='HMR')


@pytest.mark.parametrize("force_field_type", ["openff", "gaff", "espaloma"])
def test_cmd_Parameterize(force_field_type):
    """Run the ``parameterize`` CLI and check that it uses the requested force field."""
    if force_field_type == "espaloma":
        pytest.importorskip("espaloma", reason="espaloma is not installed")
    executable = shutil.which("parameterize")
    if executable is None:
        pytest.fail("The 'parameterize' command is not on PATH; is TOFF installed?")

    config = {**config_dict, 'force_field_type': force_field_type, 'mol_resi_name': force_field_type[:3].upper()}
    config_file = os.path.join(tmp_dir.name, f'config_{force_field_type}.yml')
    with open(config_file, 'w') as f:
        yaml.dump(config, f)

    # Full path to TOFF's own entry point, no shell, no external input
    process = subprocess.run([executable, config_file], capture_output=True, text=True, check=False)  # nosec B603
    if process.returncode != 0:
        raise RuntimeError(process.stderr)
    # Regression test: older CLIs dropped force_field_type and silently used OpenFF
    if f"Parameterizing with {force_field_type}" not in process.stdout:
        pytest.fail(f"The CLI did not use {force_field_type}. Its output was:\n{process.stdout}")


if __name__ == '__main__':
    pass
