#!/usr/bin/env bash
# Minimal antechamber reproducer: RDKit/OpenFF write ethane, antechamber reads it (as OpenFF/openmmforcefields do).
# Written to investigate GAFF failing on macOS Intel: there antechamber randomly reads zero atoms from a
# valid SDF (2026-11: ~20-25% of calls, AmberTools 24.8 and 26.0). Disabled in CI; to re-check, uncomment its
# step in .github/workflows/tests.yml.
# Portable to macOS (BSD tools): uses `od -c`, not `cat -A`. Never aborts: every step reports and continues.
# Run with the conda environment active (needs $CONDA_PREFIX, python with rdkit, and ambertools).
set -u

section() { printf '\n========== %s ==========\n' "$*"; }

workdir="$(mktemp -d)"
cd "$workdir" || exit 1
echo "Working directory: $workdir"

section "Platform"
uname -a
locale
echo "CONDA_PREFIX=${CONDA_PREFIX:-<unset>}"

section "AmberTools build"
for f in "$CONDA_PREFIX"/conda-meta/ambertools-*.json; do
    python -c "import json, sys; d = json.load(open(sys.argv[1])); print(d['name'], d['version'], d['build'], d.get('channel', ''))" "$f"
done
for prog in antechamber sqm; do
    for p in "$CONDA_PREFIX/bin/$prog" "$CONDA_PREFIX/bin/wrapped_progs/$prog"; do
        [[ -e "$p" ]] || continue
        echo "--- $p"
        command -v file >/dev/null && file "$p"
        if command -v otool >/dev/null; then otool -L "$p"; elif command -v ldd >/dev/null; then ldd "$p"; fi
    done
done

section "Write ethane with RDKit (SDF and PDB)"
python - <<'EOF'
from rdkit import Chem
from rdkit.Chem import AllChem
mol = Chem.AddHs(Chem.MolFromSmiles("CC"))
AllChem.EmbedMolecule(mol, randomSeed=1)
Chem.MolToMolFile(mol, "molecule.sdf")
Chem.MolToPDBFile(mol, "molecule.pdb")
EOF
ls -l molecule.sdf molecule.pdb

section "molecule.sdf with visible line endings (od -c)"
od -c molecule.sdf | head -40

# Each case runs in its own directory so the intermediate files do not mix.
run_case() {
    local name="$1"; shift
    section "antechamber: $name"
    mkdir -p "$name"
    cp molecule.sdf molecule.pdb "$name"/
    (
        cd "$name" || exit 1
        echo "+ antechamber $*"
        antechamber "$@" -pf no -dr n
        echo "exit code: $?"
        ls -l
        for f in ANTECHAMBER_AC.AC0 out.mol2 sqm.in sqm.out; do
            [[ -f "$f" ]] || continue
            echo "--- $f"
            cat -v "$f"
        done
    )
}

# 1. Does antechamber read the molecule at all without charges (no sqm)?
run_case sdf-nocharge -i molecule.sdf -fi sdf -o out.mol2 -fo mol2
# 2. Is it only the SDF reader?
run_case mdl-nocharge -i molecule.sdf -fi mdl -o out.mol2 -fo mol2
run_case pdb-nocharge -i molecule.pdb -fi pdb -o out.mol2 -fo mol2
# The failing command (as OpenFF runs it), and the same from PDB
run_case sdf-bcc -i molecule.sdf -fi sdf -o out.mol2 -fo mol2 -c bcc -nc 0
run_case pdb-bcc -i molecule.pdb -fi pdb -o out.mol2 -fo mol2 -c bcc -nc 0

# Repeat the exact commands OpenFF/openmmforcefields run, each time on a fresh conformer, to catch
# intermittent failures: in CI, the same molecule passes on one call and fails on the next.
section "Stress test: OpenFF/openmmforcefields antechamber commands, repeated"
N_REPEATS="${N_REPEATS:-20}" python - <<'EOF'
import os
import subprocess
import tempfile

from openff.toolkit import Molecule

n = int(os.environ["N_REPEATS"])
commands = {
    # OpenFF AmberToolsToolkitWrapper.assign_partial_charges (am1bcc)
    "bcc": "antechamber -i molecule.sdf -fi sdf -o charged.mol2 -fo mol2 -pf yes -dr n -c bcc -nc 0.0",
    # openmmforcefields GAFFTemplateGenerator._run_antechamber (atom typing, no charges)
    "gaff2": "antechamber -i molecule.sdf -fi mdl -o out.mol2 -fo mol2 -s 0 -at gaff2 -dr no",
}
failures = {key: 0 for key in commands}


def gaff_types(mol2, n_atoms):
    """Atom types as openmmforcefields reads them: fixed columns 50-58 of the ATOM block."""
    with open(mol2) as f:
        lines = f.read().splitlines()
    start = lines.index("@<TRIPOS>ATOM") + 1
    return [(lines[i] if i < len(lines) else "")[50:58].strip() for i in range(start, start + n_atoms)]


for i in range(1, n + 1):
    molecule = Molecule.from_smiles("CC")
    molecule.generate_conformers(n_conformers=1)
    for key, cmd in commands.items():
        with tempfile.TemporaryDirectory() as tmp:
            molecule.to_file(os.path.join(tmp, "molecule.sdf"), file_format="sdf")
            proc = subprocess.run(cmd.split(), cwd=tmp, capture_output=True, text=True)
            mol2 = os.path.join(tmp, cmd.split()[cmd.split().index("-o") + 1])
            problem = None
            if proc.returncode != 0:
                problem = f"exit code {proc.returncode}"
            elif not os.path.exists(mol2):
                problem = "no output mol2"
            elif key == "gaff2" and "" in (types := gaff_types(mol2, molecule.n_atoms)):
                problem = f"empty atom type(s): {types}"
            if problem is None:
                continue
            failures[key] += 1
            print(f"\n----- run {i} / {key}: FAILED ({problem})")
            print(f"+ {cmd}")
            print("--- stdout/stderr:\n" + proc.stdout + proc.stderr)
            for name in ("molecule.sdf", os.path.basename(mol2), "ANTECHAMBER_AC.AC0", "sqm.in", "sqm.out"):
                path = os.path.join(tmp, name)
                if os.path.exists(path):
                    with open(path, errors="replace") as f:
                        print(f"--- {name}:\n{f.read()}")

print(f"\nSummary over {n} runs: " + ", ".join(f"{k}: {v} failed" for k, v in failures.items()))
EOF

exit 0
