"""Config flow to configure the Solutions3000 integration."""
from __future__ import annotations

from typing import Any

import voluptuous as vol

from .solutions3000 import Panel, UserType, PanelException

from homeassistant.config_entries import ConfigEntry, ConfigFlow
from homeassistant.const import CONF_PORT, CONF_IP_ADDRESS, CONF_PIN, CONF_PASSWORD, CONF_NAME
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN


class Solutions3000FlowHandler(ConfigFlow, domain=DOMAIN):
    """Config flow for Solutions3000."""

    VERSION = 1

    entry: ConfigEntry | None = None

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
                    user_type=UserType.InstallerApp,
                    passcode=user_input[CONF_PASSWORD],
                    pincode=user_input[CONF_PIN]
                )
                await panel.initialise()
                panel.close()
            except PanelException as e:
                errors["base"] = " ".join(str(r) for r in e.args)
            else:
                return self.async_create_entry(
                    title=user_input[CONF_NAME],
                    data={
                        CONF_PORT: user_input[CONF_PORT],
                        CONF_IP_ADDRESS: user_input[CONF_IP_ADDRESS],
                        CONF_PASSWORD: user_input[CONF_PASSWORD],
                        CONF_PIN: user_input[CONF_PIN],
                    },
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_PORT): str,
                    vol.Required(CONF_IP_ADDRESS): str,
                    vol.Required(CONF_PASSWORD): str,
                    vol.Required(CONF_PIN): int,
                    vol.Optional(
                        CONF_NAME, default=self.hass.config.location_name
                    ): str,
                }
            ),
            errors=errors,
        )
