"""Support for Solution3000 sensors."""
from __future__ import annotations

from homeassistant.components.switch import (
    DOMAIN as COMPONENT_DOMAIN,
    SwitchEntity,
    SwitchEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import DOMAIN

from .solution3000 import Output, OutputStatus, Panel


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Solution3000 sensors based on a config entry."""
    async_add_entities(
        Solution3000OutputEntity(
            coordinator=hass.data[DOMAIN][entry.entry_id],
            entry_id=entry.entry_id,
            output=output,
        )
        for output in hass.data[DOMAIN][entry.entry_id].data.outputs
    )


class Solution3000OutputEntity(CoordinatorEntity, SwitchEntity):
    """Defines an Solution3000 sensor."""

    def __init__(
        self,
        *,
        coordinator: DataUpdateCoordinator[Panel],
        entry_id: str,
        output: Output,
    ) -> None:
        """Initialize Solution3000 sensor."""
        super().__init__(coordinator=coordinator)
        self.output = output
        self.entity_id = f"{COMPONENT_DOMAIN}.output_{output.id}"
        self._attr_unique_id = f"{COMPONENT_DOMAIN}_{entry_id}_{output.id}"
        self._attr_name = f"{output.name}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, f"{COMPONENT_DOMAIN}_{entry_id}")},
            manufacturer="Bosch",
            model=coordinator.data.panel_type_name(),
            name=f"{output.name}",
        )

    @property
    def is_on(self) -> bool:
        return self.output.status == OutputStatus.Active

    async def async_turn_on(self, **kwargs):
        self.coordinator.data.set_output(self.output, OutputStatus.Active)

    async def async_turn_off(self, **kwargs):
        self.coordinator.data.set_output(self.output, OutputStatus.Inactive)
