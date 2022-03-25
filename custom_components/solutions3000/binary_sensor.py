"""Support for Solution3000 sensors."""
from __future__ import annotations

from homeassistant.components.binary_sensor import (
    DOMAIN as COMPONENT_DOMAIN,
    BinarySensorEntity,
    BinarySensorEntityDescription,
    DEVICE_CLASS_MOTION,
    DEVICE_CLASS_SMOKE
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

from .solution3000 import Panel, Point, Area, PointStatus


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Solution3000 sensors based on a config entry."""
    async_add_entities(
        Solution3000SensorEntity(
            coordinator=hass.data[DOMAIN][entry.entry_id],
            entry_id=entry.entry_id,
            area=area,
            point=point,
        )
        for area in hass.data[DOMAIN][entry.entry_id].data.areas
        for point in area.points
    )


class Solution3000SensorEntity(CoordinatorEntity, BinarySensorEntity):
    """Defines an Solution3000 sensor."""

    def __init__(
        self,
        *,
        coordinator: DataUpdateCoordinator[Panel],
        entry_id: str,
        area: Area,
        point: Point,
    ) -> None:
        """Initialize Solution3000 sensor."""
        super().__init__(coordinator=coordinator)
        self.point = point
        self.area = area
        self.entity_id = f"{COMPONENT_DOMAIN}.{area.id}_{point.id}"
        self._attr_unique_id = f"{COMPONENT_DOMAIN}_{entry_id}_{area.id}_{point.id}"
        self._attr_name = f"{point.name}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, f"{entry_id}_{area.name}")},
            manufacturer="Bosch",
            model=coordinator.data.panel_type_name(),
            name=f"{area.name}",
        )

    @property
    def device_class(self):
        return DEVICE_CLASS_MOTION

    @property
    def is_on(self) -> StateType:
        """Return the state of the sensor."""
        return self.point.status == PointStatus.Open

    @property
    def extra_state_attributes(self):
        return {"extended_status": self.point.status.name}