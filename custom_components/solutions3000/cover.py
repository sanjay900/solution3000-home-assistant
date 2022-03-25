"""Support for Solution3000 sensors."""
from __future__ import annotations

from homeassistant.components.cover import (
    DOMAIN as COMPONENT_DOMAIN,
    CoverEntity,
    CoverEntityDescription,
    DEVICE_CLASS_DOOR,
    SUPPORT_OPEN,
    SUPPORT_CLOSE
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

from .solution3000 import DoorState, Door, Door


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Solution3000 sensors based on a config entry."""
    async_add_entities(
        Solution3000CoverEntity(
            coordinator=hass.data[DOMAIN][entry.entry_id],
            entry_id=entry.entry_id,
            door=door,
        )
        for door in hass.data[DOMAIN][entry.entry_id].data.doors
    )


class Solution3000CoverEntity(CoordinatorEntity, CoverEntity):
    """Defines an Solution3000 door."""

    def __init__(
        self,
        *,
        coordinator: DataUpdateCoordinator,
        entry_id: str,
        door: Door,
    ) -> None:
        """Initialize Solution3000 sensor."""
        super().__init__(coordinator=coordinator)
        self.door = door
        self.entity_id = f"{COMPONENT_DOMAIN}.door_{door.id}"
        self._attr_unique_id = f"{COMPONENT_DOMAIN}_{entry_id}_{door.id}"
        self._attr_name = f"Door: {door.name}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, f"{COMPONENT_DOMAIN}_{entry_id}")},
            manufacturer="bosch",
            model="solutions 3000",
            name=f"{door.name}",
        )

    @property
    def supported_features(self) -> int | None:
        return SUPPORT_OPEN | SUPPORT_CLOSE

    @property
    def is_closed(self) -> bool:
        return self.door.is_secured()
    
    @property
    def device_class(self) -> str | None:
        return DEVICE_CLASS_DOOR

    async def async_open_cover(self, **kwargs):
        current_mask = self.door.status
        current_mask &= DoorState.Secure
        self.coordinator.data.set_door(self.output, current_mask)

    async def async_close_cover(self, **kwargs):
        current_mask = self.door.status
        current_mask &= DoorState.UnlockDoor
        self.coordinator.data.set_door(self.output, current_mask)
