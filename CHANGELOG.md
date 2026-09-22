# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [0.3.2] - 2026-09-22

### Fixed

- Avoid importing the native HomeKit integration's private constants module
  during config-flow discovery. This prevents Home Assistant from rejecting the
  flow with `Invalid handler specified` when that private module's exports differ
  between Home Assistant releases.

## [0.3.1] - 2026-09-20

### Fixed

- Import the HomeKit-specific `CONF_PIN_CODE` constant from the native HomeKit
  integration instead of the Home Assistant global constants module, restoring
  compatibility with Home Assistant versions where that constant is no longer
  globally exported.

## [0.3.0] - 2026-09-20

### Added

- Reconfiguration flows for changing the domain or integration exported by an
  existing child bridge.
- One pairing-code sensor per integration instance, backed by the same setup code
  supplied to Home Assistant's native HomeKit bridge.
- Automatic generation of valid, random HomeKit setup codes for both new and
  upgraded entries.

### Changed

- Reconfiguring an instance now synchronizes and reloads its managed native
  HomeKit entry while preserving its assigned port and entry identity.

## [0.2.0] - 2026-09-20

### Fixed

- Include a unique port when importing each managed bridge into Home Assistant's
  native HomeKit integration. This prevents setup from failing with
  `KeyError: 'port'` on Home Assistant versions that require the port in import
  data.

## [0.1.0] - 2026-09-20

### Added

- A configuration flow for creating groups by domain or integration.
- A separate native HomeKit bridge for every group.
- Independent QR codes and pairing provided by Home Assistant.
- Automatic removal of a managed HomeKit bridge when its group is deleted.
- English, Spanish, German, Italian, French, and Portuguese configuration UI
  strings.
- HACS installation metadata.
- A manifest issue tracker for HACS validation.
- Hassfest-compatible manifest key ordering.
- Correct space-delimited HACS exclusions for GitHub-managed repository metadata
  and external brand assets.
- Battery Devices Monitor-style `ci.yaml` and `validate.yaml` GitHub Actions for
  tests, linting, Home Assistant validation, and HACS validation.
- Management of grouped bridges in place of direct group configuration through
  the base `homekit` integration.
- English base documentation for installation, configuration, and development.

[0.1.0]: https://github.com/Geek-MD/HomeKit_Bridge/releases/tag/v0.1.0
[0.2.0]: https://github.com/Geek-MD/HomeKit_Bridge/releases/tag/v0.2.0
[0.3.0]: https://github.com/Geek-MD/HomeKit_Bridge/releases/tag/v0.3.0
[0.3.1]: https://github.com/Geek-MD/HomeKit_Bridge/releases/tag/v0.3.1
[0.3.2]: https://github.com/Geek-MD/HomeKit_Bridge/releases/tag/v0.3.2
