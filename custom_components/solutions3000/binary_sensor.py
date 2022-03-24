"""Support for Solutions3000 sensors."""
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

from .solutions3000 import Point, Area, PointStatus


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Solutions3000 sensors based on a config entry."""
    async_add_entities(
        Solutions3000SensorEntity(
            coordinator=hass.data[DOMAIN][entry.entry_id],
            entry_id=entry.entry_id,
            area=area,
            point=point,
        )
        for area in hass.data[DOMAIN][entry.entry_id].data.areas
        for point in area.points
    )


class Solutions3000SensorEntity(CoordinatorEntity, BinarySensorEntity):
    """Defines an Solutions3000 sensor."""

    def __init__(
        self,
        *,
        coordinator: DataUpdateCoordinator,
        entry_id: str,
        area: Area,
        point: Point,
    ) -> None:
        """Initialize Solutions3000 sensor."""
        super().__init__(coordinator=coordinator)
        self.point = point
        self.area = area
        self.entity_id = f"{COMPONENT_DOMAIN}.{area.id}_{point.id}"
        self._attr_unique_id = f"{COMPONENT_DOMAIN}_{entry_id}_{area.id}_{point.id}"
        self._attr_name = f"{area.name} - {point.name}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, f"{entry_id}_{area.name}")},
            manufacturer="bosch",
            model="solutions 3000",
            name=f"{area.name} sensors",
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