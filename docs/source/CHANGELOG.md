# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [unreleased]

## [0.0.2]

### Added

- `toff.utils.get_rdkit_mol` accept `sdf` molecules too. Only the first molecule/conformer will be used.
- Example using the `safe_naming_prefix` on `toff.utils.Parameterize`.

## [0.0.1] - 2023.01.08

### Changed

- `toff.utils.confgen` now check if it is needed to generate a conformation and add hydrogens.

### Removed

- Parameter `gen_conformer` from `toff.utils.get_rdkit_mol` and `toff.utils.parameterize.__call__`.

### Added

- `toff.utils.safe_naming`. Add a prefix to the atom types.
- `safe_naming_prefix` keyword on `toff.utils.Parameterize`. It uses the previous function if some string is provided.
- `max_iter` to `toff.utils.charge_sanitizer`. Maximum number of iteration in case of charge correction.

### Fixed

- Improve documentation

[unreleased]: https://github.com/ale94mleon/TOFF/compare/0.0.2...HEAD
[unreleased]: https://github.com/ale94mleon/TOFF/compare/0.0.1...0.0.2
[0.0.1]: https://github.com/ale94mleon/TOFF/compare/0.0.0-alpha2...0.0.1