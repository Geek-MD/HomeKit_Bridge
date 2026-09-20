# HomeKit Child Bridge

[![CI](https://github.com/Geek-MD/HomeKit_Bridge/actions/workflows/ci.yaml/badge.svg)](https://github.com/Geek-MD/HomeKit_Bridge/actions/workflows/ci.yaml)
[![Validate](https://github.com/Geek-MD/HomeKit_Bridge/actions/workflows/validate.yaml/badge.svg)](https://github.com/Geek-MD/HomeKit_Bridge/actions/workflows/validate.yaml)
[![HACS](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://hacs.xyz/)

A custom Home Assistant integration that publishes groups of entities as separate
Apple Home bridges. Each entry creates a native `homekit` entry, so Home Assistant
provides an independent QR code and pairing code for every group.

## Version 0.3.1

This README documents **HomeKit Child Bridge 0.3.1**. This patch release restores
startup on current Home Assistant versions while retaining reconfiguration and
the sensor containing each instance's Apple Home pairing code.

### Requirements

- Home Assistant 2025.1.0 or newer.
- The built-in HomeKit integration.
- An Apple Home hub is recommended for remote access and automations.

### Features

- Export all entities from a domain (`light`, `cover`, and so on).
- Export the entities that belong to a configured integration.
- Create an independent HomeKit bridge for every selection.
- Configure multiple instances, each with its own bridge, port, and pairing code.
- Reconfigure an existing instance without replacing its managed bridge.
- Read the Apple Home setup code from the instance's pairing-code sensor.
- Automatically remove the managed bridge when its group is deleted.
- Reuse Home Assistant's built-in HomeKit implementation instead of running an
  alternative HAP server.
- Configuration UI translations for English, Spanish, German, Italian, French,
  and Portuguese.

This integration replaces the need to configure groups directly through the base
`homekit` integration. Its manifest declares `homekit` as a dependency, and the
integration uses Home Assistant's native HAP implementation internally to retain
compatibility with Home Assistant and Apple Home.

See the [0.3.1 changelog](CHANGELOG.md#031---2026-09-20) for the complete release
notes.

### Installation

#### HACS

1. Add this repository to HACS as a custom integration repository.
2. Search for **HomeKit Child Bridge** and install version **0.3.1**.
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

Home Assistant's native HomeKit integration presents the QR code while an
unpaired bridge is ready for pairing. The same numeric setup code remains
available in the **Pairing code** sensor created under the HomeKit Child Bridge
device.

To change an instance later, open **Settings → Devices & services**, select its
HomeKit Child Bridge entry, open the overflow menu, and choose **Reconfigure**.
You can add further instances from **Add integration**; an exported group can only
belong to one instance.

> Do not configure the same entities in multiple HomeKit bridges. Apple Home will
> display them as duplicates.

### Supported languages

Version 0.3.1 includes configuration UI translations for:

- English
- French
- German
- Italian
- Portuguese
- Spanish

## Development for 0.3.1

```bash
python -m pip install -e '.[test]'
pytest
ruff check .
```

The integration version is defined in
`custom_components/homekit_child_bridge/manifest.json`. Any behavior added after
0.3.1 must be documented in the changelog for its corresponding release.

Pull requests and pushes are checked by the same `ci.yaml` and `validate.yaml`
workflows used by Battery Devices Monitor. They run Ruff, pytest, hassfest, and
HACS validation; validation is also scheduled daily.

## License

MIT
