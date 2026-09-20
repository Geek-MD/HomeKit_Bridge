"""Create independently paired HomeKit bridges from entity groups."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.homekit.const import CONF_PIN_CODE
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME, CONF_PORT, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from .const import (
    CONF_CHILD_ENTRY_ID,
    CONF_GROUP_TYPE,
    CONF_PAIRING_CODE,
    CONF_SOURCE,
    GROUP_DOMAIN,
    HOMEKIT_DOMAIN,
    generate_pairing_code,
    next_homekit_port,
)

_LOGGER = logging.getLogger(__name__)
PLATFORMS = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Ensure the native HomeKit child bridge exists."""
    if CONF_PAIRING_CODE not in entry.data:
        hass.config_entries.async_update_entry(
            entry,
            data={**entry.data, CONF_PAIRING_CODE: generate_pairing_code()},
        )

    child_id = entry.data.get(CONF_CHILD_ENTRY_ID)
    if child_id and (child := hass.config_entries.async_get_entry(child_id)):
        homekit_data = _homekit_config(hass, entry, child.data.get(CONF_PORT))
        updated_child_data = {**child.data, **homekit_data}
        if child.data != updated_child_data or child.title != entry.title:
            hass.config_entries.async_update_entry(
                child, data=updated_child_data, title=entry.title
            )
            await hass.config_entries.async_reload(child.entry_id)
        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
        return True

    homekit_data = _homekit_config(hass, entry)
    result = await hass.config_entries.flow.async_init(
        HOMEKIT_DOMAIN,
        context={"source": "import"},
        data=homekit_data,
    )
    child = result.get("result")
    if child is None:
        _LOGGER.error("HomeKit did not create a bridge for %s: %s", entry.title, result)
        return False

    hass.config_entries.async_update_entry(
        entry,
        data={**entry.data, CONF_CHILD_ENTRY_ID: child.entry_id},
    )
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload entities while the native HomeKit entry keeps running."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_remove_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Remove the native bridge owned by a deleted group."""
    if child_id := entry.data.get(CONF_CHILD_ENTRY_ID):
        if hass.config_entries.async_get_entry(child_id):
            await hass.config_entries.async_remove(child_id)


def _homekit_config(
    hass: HomeAssistant, entry: ConfigEntry, port: int | None = None
) -> dict[str, Any]:
    """Translate a group entry into Home Assistant's native HomeKit filter."""
    source = entry.data[CONF_SOURCE]
    if entry.data[CONF_GROUP_TYPE] == GROUP_DOMAIN:
        entity_filter = {"include_domains": [source]}
    else:
        registry = er.async_get(hass)
        entity_filter = {
            "include_entities": sorted(
                entity.entity_id
                for entity in registry.entities.values()
                if entity.config_entry_id == source and entity.disabled_by is None
            )
        }

    return {
        CONF_NAME: entry.title,
        CONF_PORT: port if isinstance(port, int) else _available_homekit_port(hass),
        CONF_PIN_CODE: entry.data[CONF_PAIRING_CODE],
        "filter": entity_filter,
        "entity_config": {},
        "mode": "bridge",
    }


def _available_homekit_port(hass: HomeAssistant) -> int:
    """Choose a port that is not assigned to another native HomeKit entry."""
    used_ports = {
        port
        for homekit_entry in hass.config_entries.async_entries(HOMEKIT_DOMAIN)
        if isinstance((port := homekit_entry.data.get(CONF_PORT)), int)
    }
    return next_homekit_port(used_ports)
