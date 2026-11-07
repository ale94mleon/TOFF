# 💿 Installation

```bash
micromamba create -n TOFF -c conda-forge parmed openff-toolkit openmm openmmforcefields importlib-resources "espaloma=>0.3.2" -y
micromamba activate TOFF
pip install toff
```

````{note}
**Espaloma on newer Linux systems.** On Linux distributions with glibc 2.41 or newer
(e.g. Ubuntu 26.04, Debian 13; check with `ldd --version`), `import espaloma` can fail with
`libtorch_cpu.so: cannot enable executable stack`. Espaloma requires an older PyTorch whose
library is mislabeled as needing an executable stack, which newer glibc refuses to load.
Fix it once, with your TOFF environment active:

```bash
micromamba activate TOFF
micromamba install -c conda-forge patchelf
patchelf --clear-execstack "$CONDA_PREFIX/lib/libtorch_cpu.so"
```

This only clears the label; PyTorch itself is unchanged. It is not needed on macOS,
on older Linux systems, or if you don't use Espaloma.
````
