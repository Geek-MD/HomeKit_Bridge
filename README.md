# HomeKit Child Bridge

A custom Home Assistant integration that publishes groups of entities as separate
Apple Home bridges. Each entry creates a native `homekit` entry, so Home Assistant
provides an independent QR code and pairing code for every group.

## Features

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

See [CHANGELOG.md](CHANGELOG.md) for the history of each release.

## Installation

1. Copy `custom_components/homekit_child_bridge` into Home Assistant's
   `custom_components` directory.
2. Restart Home Assistant.
3. Go to **Settings → Devices & services → Add integration** and search for
   **HomeKit Child Bridge**.
4. Choose whether to group entities by domain or integration, then select the
   group to export.
5. Open the new **HomeKit Bridge** entry created by Home Assistant and scan its QR
   code.

> Do not configure the same entities in multiple HomeKit bridges. Apple Home will
> display them as duplicates.

## Development

```bash
python -m pip install -e '.[test]'
pytest
ruff check .
```

## License

MIT
