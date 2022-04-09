"""Config flow to configure the Solution3000 integration."""
from __future__ import annotations
from ipaddress import ip_address

from typing import Any

import voluptuous as vol

from .solution3000 import Panel, UserType, PanelException

from homeassistant.config_entries import ConfigEntry, ConfigFlow, OptionsFlow, callback
from homeassistant.const import (
    CONF_PORT,
    CONF_IP_ADDRESS,
    CONF_PIN,
    CONF_PASSWORD,
    CONF_NAME,
)
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN, CONF_HISTORY, CONF_HISTORY_COUNT

class OptionsFlowHandler(OptionsFlow):
    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_HISTORY,
                        default=self.config_entry.options.get(CONF_HISTORY),
                    ): bool,

                    vol.Required(
                        CONF_HISTORY_COUNT,
                        default=self.config_entry.options.get(CONF_HISTORY_COUNT),
                    ): int
                }
            ),
        )

class Solution3000FlowHandler(ConfigFlow, domain=DOMAIN):
    """Config flow for Solution3000."""

    VERSION = 2

    entry: ConfigEntry | None = None

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return OptionsFlowHandler(config_entry)

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle a flow initialized by the user."""
        errors = {}

        if user_input is not None:
            try:
                panel = Panel(
                    port=user_input[CONF_PORT],
                    ip=user_input[CONF_IP_ADDRESS],
                    pincode=user_input[CONF_PIN],
                    show_history=False,
                    history_count=20
                )
                await panel.initialise()
                await panel.close()
            except PanelException as e:
                print(e)
                errors["base"] = " ".join(str(r) for r in e.args)
            else:
                return self.async_create_entry(
                    title=user_input[CONF_NAME],
                    data={
                        CONF_PORT: user_input[CONF_PORT],
                        CONF_IP_ADDRESS: user_input[CONF_IP_ADDRESS],
                        CONF_PIN: user_input[CONF_PIN],
                    },
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Optional(CONF_PORT, default=7700): int,
                    vol.Required(CONF_IP_ADDRESS): str,
                    vol.Required(CONF_PIN): int,
                    vol.Optional(
                        CONF_NAME, default=self.hass.config.location_name
                    ): str
                }
            ),
            errors=errors,
        )
