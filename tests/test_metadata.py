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


def _keys(value: object, prefix: str = "") -> set[str]:
    """Return every nested mapping key as a dotted path."""
    if not isinstance(value, dict):
        return set()
    return {
        path
        for key, child in value.items()
        for path in ({f"{prefix}{key}"} | _keys(child, f"{prefix}{key}."))
    }


def test_all_translations_match_base_strings() -> None:
    """Every supported language must provide the complete base string structure."""
    base = _json(INTEGRATION / "strings.json")

    for language in ("de", "es", "fr", "it", "pt"):
        translation = _json(INTEGRATION / "translations" / f"{language}.json")
        assert _keys(translation) == _keys(base), language
