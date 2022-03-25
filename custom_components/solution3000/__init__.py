from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import (
    Platform,
    CONF_PORT,
    CONF_IP_ADDRESS,
    CONF_PIN,
    CONF_PASSWORD,
)
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .solution3000 import Panel, UserType, ArmType
from .const import DOMAIN, LOGGER, SERVICE_PANEL, SCAN_INTERVAL

# List of platforms to support. There should be a matching .py file for each,
# eg <cover.py> and <sensor.py>
PLATFORMS: list[str] = [Platform.BINARY_SENSOR, Platform.ALARM_CONTROL_PANEL, Platform.COVER, Platform.SWITCH]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    panel = Panel(
        entry.data[CONF_PORT],
        entry.data[CONF_IP_ADDRESS],
        UserType.InstallerApp,
        entry.data[CONF_PASSWORD],
        entry.data[CONF_PIN],
    )
    await panel.initialise()
    panel_update: DataUpdateCoordinator[Panel] = DataUpdateCoordinator(
        hass,
        LOGGER,
        name=f"{DOMAIN}_{SERVICE_PANEL}",
        update_interval=SCAN_INTERVAL,
        update_method=panel.update_status,
    )
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = panel_update
    await panel_update.async_config_entry_first_refresh()

    # It's done by calling the `async_setup_entry` function in each platform module.
    hass.config_entries.async_setup_platforms(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # This is called when an entry/configured device is to be removed. The class
    # needs to unload itself, and remove callbacks. See the classes for further
    # details
    hass.data[DOMAIN][entry.entry_id].close()
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
