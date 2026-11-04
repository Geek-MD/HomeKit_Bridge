"""Config flow for HomeKit Child Bridge."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.selector import SelectOptionDict, SelectSelector, SelectSelectorConfig

from .const import (
    CONF_CHILD_ENTRY_ID,
    CONF_GROUP_TYPE,
    CONF_INCLUDE_ENTITY_GROUPS,
    CONF_PAIRING_CODE,
    CONF_SOURCE,
    DOMAIN,
    GROUP_DOMAIN,
    GROUP_INTEGRATION,
    generate_pairing_code,
)


class HomeKitChildBridgeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Configure one independently paired HomeKit bridge."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Choose the source and entity-group policy."""
        if user_input is not None:
            return await self._async_finish(user_input)

        return self._show_bridge_form("user")

    async def async_step_reconfigure(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Reconfigure an existing child bridge."""
        entry = self._get_reconfigure_entry()
        self.context["reconfigure_entry_id"] = entry.entry_id
        if user_input is not None:
            return await self._async_finish(user_input)

        return self._show_bridge_form("reconfigure", entry)

    def _show_bridge_form(
        self, step_id: str, entry: config_entries.ConfigEntry | None = None
    ) -> config_entries.ConfigFlowResult:
        """Show source selection and group policy together."""
        options = self._source_options()
        selection_field = (
            vol.Required(
                CONF_SOURCE,
                default=f"{entry.data[CONF_GROUP_TYPE]}:{entry.data[CONF_SOURCE]}",
            )
            if entry
            else vol.Required(CONF_SOURCE)
        )
        return self.async_show_form(
            step_id=step_id,
            data_schema=vol.Schema(
                {
                    selection_field: SelectSelector(
                        SelectSelectorConfig(
                            options=[
                                SelectOptionDict(value=value, label=label)
                                for value, label in options
                            ],
                            mode="dropdown",
                        )
                    ),
                    vol.Required(
                        CONF_INCLUDE_ENTITY_GROUPS,
                        default=(
                            entry.data.get(CONF_INCLUDE_ENTITY_GROUPS, True) if entry else False
                        ),
                    ): bool,
                }
            ),
        )

    async def _async_finish(self, user_input: dict[str, Any]) -> config_entries.ConfigFlowResult:
        """Create or update a bridge from the combined source selection."""
        selection = user_input[CONF_SOURCE]
        group_type, source = selection.split(":", 1)
        include_entity_groups = user_input[CONF_INCLUDE_ENTITY_GROUPS]
        label = dict(self._source_options()).get(selection, source)
        unique_id = selection

        if entry_id := self.context.get("reconfigure_entry_id"):
            entry = self.hass.config_entries.async_get_entry(entry_id)
            assert entry is not None
            if any(
                candidate.entry_id != entry.entry_id and candidate.unique_id == unique_id
                for candidate in self.hass.config_entries.async_entries(DOMAIN)
            ):
                return self.async_abort(reason="already_configured")
            self.hass.config_entries.async_update_entry(
                entry, unique_id=unique_id, title=f"HomeKit · {label}"
            )
            return self.async_update_reload_and_abort(
                entry,
                data_updates={
                    CONF_GROUP_TYPE: group_type,
                    CONF_INCLUDE_ENTITY_GROUPS: include_entity_groups,
                    CONF_SOURCE: source,
                    CONF_PAIRING_CODE: entry.data.get(CONF_PAIRING_CODE, generate_pairing_code()),
                    **(
                        {CONF_CHILD_ENTRY_ID: entry.data[CONF_CHILD_ENTRY_ID]}
                        if CONF_CHILD_ENTRY_ID in entry.data
                        else {}
                    ),
                },
            )

        await self.async_set_unique_id(unique_id)
        self._abort_if_unique_id_configured()
        return self.async_create_entry(
            title=f"HomeKit · {label}",
            data={
                CONF_GROUP_TYPE: group_type,
                CONF_INCLUDE_ENTITY_GROUPS: include_entity_groups,
                CONF_SOURCE: source,
                CONF_PAIRING_CODE: generate_pairing_code(),
            },
        )

    def _source_options(self) -> list[tuple[str, str]]:
        """Return domains and integrations in one source selector."""
        registry = er.async_get(self.hass)
        domains = sorted({entry.domain for entry in registry.entities.values()})
        domain_options = [
            (
                f"{GROUP_DOMAIN}:{domain}",
                f"Domain · {domain.replace('_', ' ').title()}",
            )
            for domain in domains
        ]

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
        integration_options = sorted(
            (
                (f"{GROUP_INTEGRATION}:{entry.entry_id}", f"Integration · {entry.title}")
                for entry in entries
            ),
            key=lambda item: item[1].casefold(),
        )
        return domain_options + integration_options
