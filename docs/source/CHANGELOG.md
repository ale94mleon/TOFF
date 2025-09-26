# 🗒️ Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [unreleased]

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

[unreleased]: https://github.com/ale94mleon/TOFF/compare/0.2.1...HEAD
[0.2.1]: https://github.com/ale94mleon/TOFF/compare/0.2.1...0.2.0
[0.2.0]: https://github.com/ale94mleon/TOFF/compare/0.1.0...0.2.0
[0.1.0]: https://github.com/ale94mleon/TOFF/compare/0.0.2...0.1.0
[0.0.2]: https://github.com/ale94mleon/TOFF/compare/0.0.1...0.0.2
[0.0.1]: https://github.com/ale94mleon/TOFF/compare/0.0.0-alpha2...0.0.1