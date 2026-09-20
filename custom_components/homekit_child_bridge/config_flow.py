"""Config flow for HomeKit Child Bridge."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.selector import SelectOptionDict, SelectSelector, SelectSelectorConfig

from .const import (
    CONF_GROUP_TYPE,
    CONF_SOURCE,
    DOMAIN,
    GROUP_DOMAIN,
    GROUP_INTEGRATION,
)


class HomeKitChildBridgeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Configure one independently paired HomeKit bridge."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Choose how entities should be grouped."""
        if user_input is not None:
            return await self.async_step_source_type(user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_GROUP_TYPE): SelectSelector(
                        SelectSelectorConfig(
                            options=[GROUP_DOMAIN, GROUP_INTEGRATION],
                            translation_key="group_type",
                        )
                    )
                }
            ),
        )

    async def async_step_source_type(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Choose the domain or integration to publish."""
        group_type = self.context.get(CONF_GROUP_TYPE)
        if user_input and CONF_GROUP_TYPE in user_input:
            group_type = user_input[CONF_GROUP_TYPE]
            self.context[CONF_GROUP_TYPE] = group_type

        options = self._source_options(group_type)
        if user_input is not None and CONF_SOURCE in user_input:
            source = user_input[CONF_SOURCE]
            await self.async_set_unique_id(f"{group_type}:{source}")
            self._abort_if_unique_id_configured()
            label = dict(options).get(source, source)
            return self.async_create_entry(
                title=f"HomeKit · {label}",
                data={CONF_GROUP_TYPE: group_type, CONF_SOURCE: source},
            )

        return self.async_show_form(
            step_id="source_type",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_SOURCE): SelectSelector(
                        SelectSelectorConfig(
                            options=[
                                SelectOptionDict(value=value, label=label)
                                for value, label in options
                            ],
                            mode="dropdown",
                        )
                    )
                }
            ),
        )

    def _source_options(self, group_type: str) -> list[tuple[str, str]]:
        registry = er.async_get(self.hass)
        if group_type == GROUP_DOMAIN:
            domains = sorted({entry.domain for entry in registry.entities.values()})
            return [(domain, domain.replace("_", " ").title()) for domain in domains]

        used_entry_ids = {
            entry.config_entry_id
            for entry in registry.entities.values()
            if entry.config_entry_id is not None
        }
        entries = [
            entry
            for entry in self.hass.config_entries.async_entries()
            if entry.entry_id in used_entry_ids and entry.domain not in {DOMAIN, "homekit"}
        ]
        return sorted(
            ((entry.entry_id, entry.title) for entry in entries),
            key=lambda item: item[1].casefold(),
        )
