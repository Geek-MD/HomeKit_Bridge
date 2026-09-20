# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

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
- Correct space-delimited HACS exclusions for GitHub-managed repository metadata
  and external brand assets.
- Battery Devices Monitor-style `ci.yaml` and `validate.yaml` GitHub Actions for
  tests, linting, Home Assistant validation, and HACS validation.
- Management of grouped bridges in place of direct group configuration through
  the base `homekit` integration.
- English base documentation for installation, configuration, and development.

[0.1.0]: https://github.com/Geek-MD/HomeKit_Bridge/releases/tag/v0.1.0
