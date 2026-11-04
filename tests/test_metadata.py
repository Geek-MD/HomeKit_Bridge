"""Repository-level tests that do not require a Home Assistant installation."""

from __future__ import annotations

import json
from importlib.util import module_from_spec, spec_from_file_location
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
    assert "replaces" not in manifest
    assert manifest["issue_tracker"].endswith("/HomeKit_Bridge/issues")
    assert list(manifest) == [
        "domain",
        "name",
        "codeowners",
        "config_flow",
        "dependencies",
        "documentation",
        "integration_type",
        "iot_class",
        "issue_tracker",
        "version",
    ]


def test_release_documentation_matches_manifest_version() -> None:
    """The README and changelog must describe the version shipped by the manifest."""
    version = _json(INTEGRATION / "manifest.json")["version"]
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")

    assert f"## Version {version}" in readme
    assert f"## [{version}]" in changelog


def test_homekit_pin_code_does_not_import_private_homekit_module() -> None:
    """Config-flow discovery must not depend on HomeKit's private constants."""
    integration = (INTEGRATION / "__init__.py").read_text(encoding="utf-8")
    constants = (INTEGRATION / "const.py").read_text(encoding="utf-8")

    assert "homeassistant.components.homekit.const" not in integration
    assert 'CONF_HOMEKIT_PIN_CODE = "pin_code"' in constants
    assert "CONF_HOMEKIT_PIN_CODE: entry.data[CONF_PAIRING_CODE]" in integration


def test_homekit_port_allocator_skips_ports_in_use() -> None:
    """Every managed bridge must receive a distinct native HomeKit port."""
    spec = spec_from_file_location("homekit_child_bridge_const", INTEGRATION / "const.py")
    assert spec is not None and spec.loader is not None
    module = module_from_spec(spec)
    spec.loader.exec_module(module)

    assert module.next_homekit_port(set()) == 21063
    assert module.next_homekit_port({21063, 21064, 21066}) == 21065


def test_generated_homekit_pairing_codes_are_valid() -> None:
    """Generated codes must use HomeKit's format and exclude trivial values."""
    spec = spec_from_file_location("homekit_child_bridge_const", INTEGRATION / "const.py")
    assert spec is not None and spec.loader is not None
    module = module_from_spec(spec)
    spec.loader.exec_module(module)

    codes = {module.generate_pairing_code() for _ in range(20)}
    assert all(len(code) == 10 and code[3] == code[6] == "-" for code in codes)
    assert all(code.replace("-", "").isdigit() for code in codes)
    assert codes.isdisjoint(module.INVALID_PAIRING_CODES)


def test_entity_group_detection_supports_helpers_and_yaml_groups() -> None:
    """Group helpers and unregistered groups must both be recognized."""
    spec = spec_from_file_location("homekit_child_bridge_const", INTEGRATION / "const.py")
    assert spec is not None and spec.loader is not None
    module = module_from_spec(spec)
    spec.loader.exec_module(module)

    assert module.is_entity_group("group", None)
    assert module.is_entity_group(None, ["light.one", "light.two"])
    assert module.is_entity_group(None, ())
    assert not module.is_entity_group("hue", None)
    assert not module.is_entity_group(None, "light.one")

    integration_entities = [
        "light.dining_room",
        "light.dining_room_one",
        "light.dining_room_two",
        "light.dining_room_three",
    ]
    assert module.without_entity_groups(integration_entities, ["light.dining_room"]) == [
        "light.dining_room_one",
        "light.dining_room_three",
        "light.dining_room_two",
    ]


def test_entity_group_policy_is_configurable_and_backward_compatible() -> None:
    """The config flow and HomeKit filter must implement the v0.4 group policy."""
    config_flow = (INTEGRATION / "config_flow.py").read_text(encoding="utf-8")
    integration = (INTEGRATION / "__init__.py").read_text(encoding="utf-8")
    strings = _json(INTEGRATION / "strings.json")

    assert "CONF_INCLUDE_ENTITY_GROUPS" in config_flow
    assert "vol.Required(CONF_INCLUDE_ENTITY_GROUPS, default=False)" in config_flow
    assert "entry.data.get(CONF_INCLUDE_ENTITY_GROUPS, True)" in integration
    assert 'entity_filter["exclude_entities"] = group_entity_ids' in integration
    assert "EMPTY_FILTER_ENTITY_ID" in integration
    assert "EVENT_HOMEASSISTANT_STARTED" in integration
    assert "_entity_group_members" in integration
    assert "include_entity_groups" in strings["config"]["step"]["user"]["data"]
    assert "include_entity_groups" in strings["config"]["step"]["reconfigure"]["data"]
    assert "include_entity_groups" not in strings["config"]["step"]["source_type"]["data"]


def test_github_actions_are_present() -> None:
    """The standard CI and validation workflows must remain in the repository."""
    workflows = ROOT / ".github" / "workflows"

    assert {path.name for path in workflows.iterdir()} == {"ci.yaml", "validate.yaml"}

    validation = (workflows / "validate.yaml").read_text(encoding="utf-8")
    assert "ignore: topics description brands" in validation
    assert not list(ROOT.glob("custom_components/**/*.png"))


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
