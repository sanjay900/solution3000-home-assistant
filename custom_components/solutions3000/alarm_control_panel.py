"""Support for Solution3000 sensors."""
from __future__ import annotations

from homeassistant.components.alarm_control_panel import (
    DOMAIN as COMPONENT_DOMAIN,
    AlarmControlPanelEntity,
    SUPPORT_ALARM_ARM_AWAY,
    SUPPORT_ALARM_ARM_CUSTOM_BYPASS,
    SUPPORT_ALARM_ARM_HOME,
    SUPPORT_ALARM_ARM_NIGHT,
    SUPPORT_ALARM_ARM_VACATION,
    SUPPORT_ALARM_TRIGGER,
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

from homeassistant.const import (
    STATE_ALARM_ARMED_AWAY,
    STATE_ALARM_ARMED_CUSTOM_BYPASS,
    STATE_ALARM_ARMED_HOME,
    STATE_ALARM_ARMED_NIGHT,
    STATE_ALARM_ARMED_VACATION,
    STATE_ALARM_ARMING,
    STATE_ALARM_DISARMED,
    STATE_ALARM_DISARMING,
    STATE_ALARM_PENDING,
    STATE_ALARM_TRIGGERED,
)

SUPPORTED_STATES = [
    STATE_ALARM_DISARMED,
    STATE_ALARM_ARMED_AWAY,
    STATE_ALARM_ARMED_HOME,
    STATE_ALARM_ARMED_NIGHT,
    STATE_ALARM_ARMED_VACATION,
    STATE_ALARM_ARMED_CUSTOM_BYPASS,
    STATE_ALARM_TRIGGERED,
]

from .const import DOMAIN

from .solution3000 import ArmType, Area, AreaStatus, Panel

SOLUTIONS3000_TO_ALARM_STATE = {
    AreaStatus.AllOn: STATE_ALARM_ARMED_AWAY,
    AreaStatus.PartOnDelay: STATE_ALARM_ARMED_NIGHT,
    AreaStatus.AllOnEntryDelay: STATE_ALARM_ARMING,
    AreaStatus.PartOnEntryDelay: STATE_ALARM_ARMING,
    AreaStatus.AllOnExitDelay: STATE_ALARM_ARMING,
    AreaStatus.PartOnExitDelay: STATE_ALARM_ARMING,
    AreaStatus.Disarmed: STATE_ALARM_DISARMED,
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Solution3000 sensors based on a config entry."""
    async_add_entities(
        Solution3000ControlPanelEntity(
            coordinator=hass.data[DOMAIN][entry.entry_id],
            entry_id=entry.entry_id,
            area=area,
        )
        for area in hass.data[DOMAIN][entry.entry_id].data.areas
    )


class Solution3000ControlPanelEntity(CoordinatorEntity, AlarmControlPanelEntity):
    """Defines an Solution3000 sensor."""

    def __init__(
        self,
        *,
        coordinator: DataUpdateCoordinator[Panel],
        entry_id: str,
        area: Area,
    ) -> None:
        """Initialize Solution3000 sensor."""
        super().__init__(coordinator=coordinator)
        self.area = area
        self.entity_id = f"{COMPONENT_DOMAIN}.{area.id}"
        self._attr_unique_id = f"{COMPONENT_DOMAIN}_{entry_id}_{area.id}"
        self._attr_name = f"{area.name}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, f"{entry_id}_{area.name}")},
            manufacturer="Bosch",
            model=coordinator.data.panel_type_name(),
            name=f"{area.name}",
        )

    @property
    def state(self) -> str | None:
        """Return the state of the sensor."""
        return SOLUTIONS3000_TO_ALARM_STATE[self.area.status]

    @property
    def supported_features(self) -> int:
        """Return the list of supported features."""
        return (
            SUPPORT_ALARM_ARM_HOME
            | SUPPORT_ALARM_ARM_NIGHT
            | SUPPORT_ALARM_ARM_AWAY
            | SUPPORT_ALARM_TRIGGER
        )

    async def async_alarm_disarm(self, code=None) -> None:
        """Send disarm command."""
        await self.coordinator.data.arm(ArmType.Disarmed, [self.area])

    async def async_alarm_arm_away(self, code=None) -> None:
        self.area.status = AreaStatus.AllOnExitDelay
        self.async_schedule_update_ha_state()
        await self.coordinator.data.arm(ArmType.Away, [self.area])

    async def async_alarm_arm_home(self, code=None) -> None:
        self.area.status = AreaStatus.PartOnExitDelay
        self.async_schedule_update_ha_state()
        await self.coordinator.data.arm(ArmType.Stay, [self.area])

    async def async_alarm_arm_night(self, code=None) -> None:
        self.area.status = AreaStatus.PartOnExitDelay
        self.async_schedule_update_ha_state()
        await self.coordinator.data.arm(ArmType.Stay2, [self.area])

    
    @property
    def extra_state_attributes(self):
        return {"panel_history": "\n".join([f"{message.datetime} | {message.message}" for message in self.coordinator.data.history_messages])}
