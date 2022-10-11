from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from homeassistant.const import (
    Platform,
    CONF_PORT,
    CONF_IP_ADDRESS,
    CONF_PIN,
)
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .solution3000 import Panel, UserType, ArmType
from .const import CONF_HISTORY, CONF_HISTORY_COUNT, CONF_REQUIRE_PIN, DOMAIN, LOGGER, SERVICE_PANEL, SCAN_INTERVAL

# List of platforms to support. There should be a matching .py file for each,
# eg <cover.py> and <sensor.py>
PLATFORMS: list[str] = [Platform.BINARY_SENSOR, Platform.ALARM_CONTROL_PANEL, Platform.COVER, Platform.SWITCH]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    requires_pin = False
    if CONF_REQUIRE_PIN in entry.options:
        requires_pin = entry.options[CONF_REQUIRE_PIN]
    panel = Panel(
        entry.data[CONF_PORT],
        entry.data[CONF_IP_ADDRESS],
        entry.data[CONF_PIN],
        entry.options[CONF_HISTORY],
        entry.options[CONF_HISTORY_COUNT],
        requires_pin
    )
    await panel.initialise()
    panel_update: DataUpdateCoordinator[Panel] = DataUpdateCoordinator(
        hass,
        LOGGER,
        name=f"{DOMAIN}_{SERVICE_PANEL}",
        update_interval=SCAN_INTERVAL,
        update_method=panel.update_status,
    )
    unsub_options_update_listener = entry.add_update_listener(options_update_listener)
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {"panel_update": panel_update, "unsub_options": unsub_options_update_listener}
    await panel_update.async_config_entry_first_refresh()
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # This is called when an entry/configured device is to be removed. The class
    # needs to unload itself, and remove callbacks. See the classes for further
    # details
    await hass.data[DOMAIN][entry.entry_id]["panel_update"].data.close()
    hass.data[DOMAIN][entry.entry_id]["unsub_options"]()
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok

async def options_update_listener(
    hass: HomeAssistant, config_entry: ConfigEntry
):
    """Handle options update."""
    await hass.config_entries.async_reload(config_entry.entry_id)
