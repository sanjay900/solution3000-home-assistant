"""Support for Solutions3000 sensors."""
from __future__ import annotations

from homeassistant.components.switch import (
    DOMAIN as SENSOR_DOMAIN,
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

from .solutions3000 import Output, OutputStatus


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Solutions3000 sensors based on a config entry."""
    async_add_entities(
        Solutions3000OutputEntity(
            coordinator=hass.data[DOMAIN][entry.entry_id],
            entry_id=entry.entry_id,
            output=output,
        )
        for output in hass.data[DOMAIN][entry.entry_id].data.outputs
    )


class Solutions3000OutputEntity(CoordinatorEntity, SwitchEntity):
    """Defines an Solutions3000 sensor."""

    def __init__(
        self,
        *,
        coordinator: DataUpdateCoordinator,
        entry_id: str,
        output: Output,
    ) -> None:
        """Initialize Solutions3000 sensor."""
        super().__init__(coordinator=coordinator)
        self.output = output
        self.entity_id = f"{SENSOR_DOMAIN}.output_{output.id}"
        self._attr_unique_id = f"output_{entry_id}_{output.id}"
        self._attr_name = f"Output: {output.name}"
        self._attr_device_info = DeviceInfo(
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, f"{entry_id}_{output.id}")},
            manufacturer="bosch",
            name=f"output_{output.name}",
        )

    @property
    def is_on(self) -> bool:
        return self.output.status == OutputStatus.Active

    async def async_turn_on(self, **kwargs):
        self.coordinator.data.set_output(self.output, OutputStatus.Active)

    async def async_turn_off(self, **kwargs):
        self.coordinator.data.set_output(self.output, OutputStatus.Inactive)
