"""Create independently paired HomeKit bridges from entity groups."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from .const import (
    CONF_CHILD_ENTRY_ID,
    CONF_GROUP_TYPE,
    CONF_SOURCE,
    GROUP_DOMAIN,
    HOMEKIT_DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Ensure the native HomeKit child bridge exists."""
    child_id = entry.data.get(CONF_CHILD_ENTRY_ID)
    if child_id and hass.config_entries.async_get_entry(child_id):
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
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """The native HomeKit entry owns its own runtime lifecycle."""
    return True


async def async_remove_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Remove the native bridge owned by a deleted group."""
    if child_id := entry.data.get(CONF_CHILD_ENTRY_ID):
        if hass.config_entries.async_get_entry(child_id):
            await hass.config_entries.async_remove(child_id)


def _homekit_config(hass: HomeAssistant, entry: ConfigEntry) -> dict[str, Any]:
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
        "filter": entity_filter,
        "entity_config": {},
        "mode": "bridge",
    }
