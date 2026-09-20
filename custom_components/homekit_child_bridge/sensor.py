"""Pairing-code sensor for HomeKit Child Bridge."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import CONF_PAIRING_CODE, DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the pairing-code sensor."""
    async_add_entities([HomeKitPairingCodeSensor(entry)])


class HomeKitPairingCodeSensor(SensorEntity):
    """Expose the setup code for one managed HomeKit bridge."""

    _attr_has_entity_name = True
    _attr_icon = "mdi:shield-key"
    _attr_translation_key = "pairing_code"

    def __init__(self, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        self._attr_unique_id = f"{entry.entry_id}_pairing_code"
        self._attr_native_value = entry.data[CONF_PAIRING_CODE]
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.title,
            manufacturer="Home Assistant",
            model="HomeKit Child Bridge",
        )
