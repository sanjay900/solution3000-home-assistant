"""Support for Solutions3000 sensors."""
from __future__ import annotations

from homeassistant.components.sensor import (
    DOMAIN as SENSOR_DOMAIN,
    SensorEntity,
    SensorEntityDescription,
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

from .const import DOMAIN, SENSORS, SERVICES

from .solutions3000 import Point, Area


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
            point=point
        )
        for area in hass.data[DOMAIN][entry.entry_id]
        for point in area
    )


class Solutions3000SensorEntity(CoordinatorEntity, SensorEntity):
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
        self.entity_id = f"{SENSOR_DOMAIN}.{area.id}_{point.id}"
        self._attr_unique_id = f"{entry_id}_{area.id}_{point.id}"

        self._attr_device_info = DeviceInfo(
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, f"{entry_id}_{area.id}_{point.id}")},
            manufacturer="bosch",
            name=f"{area.name}: {point.name}",
        )

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        
        return self.point.status.name()