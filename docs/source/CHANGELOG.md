# 🗒️ Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [unreleased]

## [0.3.0]-2026.11.07

### Fixed

- The `parameterize` command line interface now accepts `force_field_type` in the configuration YAML file. Previously it was discarded with a warning, so GAFF and Espaloma could not be selected from the CLI.
- The API reference was empty because autodoc could not import `toff.utils` in the docs environment; OpenMM, OpenFF and ParmEd are now mocked during the docs build.
- License metadata is declared again (`License-Expression: Apache-2.0`, PEP 639); it was missing from PyPI since 0.2.0. The README license badge now uses shields.io.
- The CLI test checks that the requested force field is used, for OpenFF, GAFF and Espaloma.

### Changed

- Minimum supported Python version is now 3.11 (`requires-python = ">=3.11"`).
- CI tests run on Python 3.11 and 3.12; coverage and the PyPI publishing workflow use Python 3.11.
- Documentation is built with Python 3.12 and current Sphinx instead of Python 3.9 and Sphinx 7.2.6; Read the Docs uses `mambaforge-latest`.
- The Binder environment uses Python 3.12.
- `toff` exports its public API explicitly (`__all__`); third-party modules are no longer re-exported from `toff` (e.g. `toff.Chem`).

### Removed

- Support for Python 3.9 and 3.10. Both versions have reached end of life, and recent OpenFF packages (`openff-amber-ff-ports >= 2025.09.0`) require Python >= 3.11. On Python 3.10 the solver falls back to `openff-amber-ff-ports 0.0.4`, which imports `pkg_resources`, removed from setuptools in version 82; this made parameterization with OpenFF fail with `ModuleNotFoundError: No module named 'pkg_resources'`.
- Unused `requirements_docs.txt`.

## [0.2.1]-2025.09.26

### Added

- Make it available on conda-forge.

### Changed

- Handle installation of ParmED at conda level.
- Update versioning.

## [0.2.0]-2025.06.19

### Added

- `pytest.ini` for better handling of warning during test.

### Changed

- Updating docs, installation instructions and improving readability.

### Fixed

- Espaloma force field is available on MacOS.
- Espaloma force field generation is handling directly and not through `openmmforcefields.generators`.
- Easy installation and dependencies handling. [micromamba](https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html) is now the preferred environment manager.
- Improve code covering and code grading.
- CI for upload to PyPi.

## [0.1.0]-2023.07.27

### Added

- {py:func}`toff.utils.generate_structure`. this function can now be used to also take parameters from GAFF and/or Espaloma. For that openmmforcefields must be installed. In the case of Espaloma, this module has to be installed as well.

### Changed

- Now the default force field in the class {py:class}`toff.utils.Parameterize` is selected base on the keyword `force_field_type`. They are:
  - openff -> openff_unconstrained-2.0.0.offxml
  - gaff -> gaff-2.11
  - espaloma -> espaloma-0.2.2

## [0.0.2]-2023.03.27

### Added

- {py:func}`toff.utils.get_rdkit_mol` accept `sdf` molecules too. Only the first molecule/conformer will be used.
- Example using the `safe_naming_prefix` on {py:class}`toff.utils.Parameterize`.

## [0.0.1]-2023.01.08

### Changed

- `toff.utils.confgen` now check if it is needed to generate a conformation and add hydrogens.

### Removed

- Parameter `gen_conformer` from {py:func}`toff.utils.get_rdkit_mol` and {py:meth}`toff.utils.parameterize.__call__`.

### Added

- {py:func}`toff.utils.safe_naming`. Add a prefix to the atom types.
- `safe_naming_prefix` keyword on {py:class}`toff.utils.Parameterize`. It uses the previous function if some string is provided.
- `max_iter` to {py:func}`toff.utils.charge_sanitizer`. Maximum number of iteration in case of charge correction.

### Fixed

- Improve documentation

[unreleased]: https://github.com/ale94mleon/TOFF/compare/0.3.0...HEAD
[0.3.0]: https://github.com/ale94mleon/TOFF/compare/0.3.0...0.2.1
[0.2.1]: https://github.com/ale94mleon/TOFF/compare/0.2.1...0.2.0
[0.2.0]: https://github.com/ale94mleon/TOFF/compare/0.1.0...0.2.0
[0.1.0]: https://github.com/ale94mleon/TOFF/compare/0.0.2...0.1.0
[0.0.2]: https://github.com/ale94mleon/TOFF/compare/0.0.1...0.0.2
[0.0.1]: https://github.com/ale94mleon/TOFF/compare/0.0.0-alpha2...0.0.1