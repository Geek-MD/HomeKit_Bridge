# HomeKit Child Bridge

A custom Home Assistant integration that publishes groups of entities as separate
Apple Home bridges. Each entry creates a native `homekit` entry, so Home Assistant
provides an independent QR code and pairing code for every group.

## Version 0.1.0

This README documents **HomeKit Child Bridge 0.1.0**, the first public release.

### Requirements

- Home Assistant 2025.1.0 or newer.
- The built-in HomeKit integration.
- An Apple Home hub is recommended for remote access and automations.

### Features

- Export all entities from a domain (`light`, `cover`, and so on).
- Export the entities that belong to a configured integration.
- Create an independent HomeKit bridge for every selection.
- Automatically remove the managed bridge when its group is deleted.
- Reuse Home Assistant's built-in HomeKit implementation instead of running an
  alternative HAP server.
- Configuration UI translations for English, Spanish, German, Italian, French,
  and Portuguese.

The manifest declares that this integration replaces direct configuration of the
base `homekit` integration. It still uses Home Assistant's native HAP implementation
internally to retain compatibility with Home Assistant and Apple Home.

See the [0.1.0 changelog](CHANGELOG.md#010---2026-09-20) for the complete release
notes.

### Installation

#### HACS

1. Add this repository to HACS as a custom integration repository.
2. Search for **HomeKit Child Bridge** and install version **0.1.0**.
3. Restart Home Assistant.

#### Manual installation

1. Copy `custom_components/homekit_child_bridge` into Home Assistant's
   `custom_components` directory.
2. Restart Home Assistant.

### Configuration

1. Go to **Settings → Devices & services → Add integration** and search for
   **HomeKit Child Bridge**.
2. Choose whether to group entities by domain or integration, then select the
   group to export.
3. Open the new **HomeKit Bridge** entry created by Home Assistant and scan its QR
   code.

> Do not configure the same entities in multiple HomeKit bridges. Apple Home will
> display them as duplicates.

### Supported languages

Version 0.1.0 includes configuration UI translations for:

- English
- French
- German
- Italian
- Portuguese
- Spanish

## Development for 0.1.0

```bash
python -m pip install -e '.[test]'
pytest
ruff check .
```

The integration version is defined in
`custom_components/homekit_child_bridge/manifest.json`. Any behavior added after
0.1.0 must be documented in the changelog for its corresponding release.

## License

MIT
