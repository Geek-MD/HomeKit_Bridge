"""Constants for HomeKit Child Bridge."""

import secrets

DOMAIN = "homekit_child_bridge"
HOMEKIT_DOMAIN = "homekit"
HOMEKIT_PORT_START = 21063

CONF_GROUP_TYPE = "group_type"
CONF_SOURCE = "source"
CONF_CHILD_ENTRY_ID = "child_entry_id"
CONF_INCLUDE_ENTITY_GROUPS = "include_entity_groups"
CONF_PAIRING_CODE = "pairing_code"

# This key is part of the data contract accepted by the native HomeKit config
# flow.  Keep it local instead of importing HomeKit's private ``const`` module:
# importing that module also happens while Home Assistant discovers our config
# flow, and constants have moved between Home Assistant releases.
CONF_HOMEKIT_PIN_CODE = "pin_code"

GROUP_DOMAIN = "domain"
GROUP_INTEGRATION = "integration"

DEFAULT_NAME = "HomeKit Child Bridge"


def is_entity_group(platform: str | None, members: object) -> bool:
    """Return whether registry and state metadata describe an entity group."""
    return platform == "group" or (
        isinstance(members, (list, tuple))
        and all(isinstance(entity_id, str) for entity_id in members)
    )


def without_entity_groups(entity_ids: list[str], group_entity_ids: list[str]) -> list[str]:
    """Return sorted individual entities while removing aggregate groups."""
    return sorted(set(entity_ids).difference(group_entity_ids))


def next_homekit_port(used_ports: set[int]) -> int:
    """Return the first HomeKit port not already assigned to a config entry."""
    port = HOMEKIT_PORT_START
    while port in used_ports:
        port += 1
    return port


INVALID_PAIRING_CODES = {
    "000-00-000",
    "111-11-111",
    "222-22-222",
    "333-33-333",
    "444-44-444",
    "555-55-555",
    "666-66-666",
    "777-77-777",
    "888-88-888",
    "999-99-999",
    "123-45-678",
    "876-54-321",
}


def generate_pairing_code() -> str:
    """Generate a valid random HomeKit setup code."""
    while True:
        digits = f"{secrets.randbelow(100_000_000):08d}"
        code = f"{digits[:3]}-{digits[3:5]}-{digits[5:]}"
        if code not in INVALID_PAIRING_CODES:
            return code
