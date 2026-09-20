"""Repository-level tests that do not require a Home Assistant installation."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).parents[1]
INTEGRATION = ROOT / "custom_components" / "homekit_child_bridge"


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_manifest_declares_config_flow_and_homekit_dependency() -> None:
    """The integration must load after the native HomeKit integration."""
    manifest = _json(INTEGRATION / "manifest.json")

    assert manifest["domain"] == "homekit_child_bridge"
    assert manifest["config_flow"] is True
    assert "homekit" in manifest["dependencies"]
    assert manifest["replaces"] == ["homekit"]


def test_spanish_translation_matches_base_flow() -> None:
    """Every flow step and selector in the base strings has a translation."""
    base = _json(INTEGRATION / "strings.json")
    spanish = _json(INTEGRATION / "translations" / "es.json")

    assert spanish["config"]["step"].keys() == base["config"]["step"].keys()
    assert spanish["selector"].keys() == base["selector"].keys()
