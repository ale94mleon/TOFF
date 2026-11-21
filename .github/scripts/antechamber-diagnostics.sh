#!/usr/bin/env bash
# Minimal antechamber reproducer, independent of TOFF/OpenFF: RDKit writes ethane, antechamber reads it.
# Used in CI to investigate GAFF failing on macOS Intel (antechamber passes zero atoms to sqm).
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

exit 0
