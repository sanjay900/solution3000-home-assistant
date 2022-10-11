"""Support for Solution3000 sensors."""
from __future__ import annotations
from .solution3000 import AlarmMemoryPriorities, ArmType, Area, AreaStatus, Panel
from .const import DOMAIN

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
import homeassistant.components.alarm_control_panel as alarm
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
    FORMAT_NUMBER,
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


SOLUTIONS3000_TO_ALARM_STATE = {
    AreaStatus.AllOn: STATE_ALARM_ARMED_AWAY,
    AreaStatus.PartOnDelay: STATE_ALARM_ARMED_NIGHT,
    AreaStatus.PartOnInstant: STATE_ALARM_ARMED_NIGHT,
    AreaStatus.AllOnEntryDelay: STATE_ALARM_PENDING,
    AreaStatus.PartOnEntryDelay: STATE_ALARM_PENDING,
    AreaStatus.AllOnExitDelay: STATE_ALARM_ARMING,
    AreaStatus.PartOnExitDelay: STATE_ALARM_ARMING,
    AreaStatus.Disarmed: STATE_ALARM_DISARMED,
    AreaStatus.StayArm1On: STATE_ALARM_ARMED_NIGHT,
    AreaStatus.StayArm2On: STATE_ALARM_ARMED_VACATION,
    AreaStatus.AwayOn: STATE_ALARM_ARMED_AWAY,
    AreaStatus.AwayExitDelay: STATE_ALARM_ARMING,
    AreaStatus.AwayEntryDelay: STATE_ALARM_PENDING
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Solution3000 sensors based on a config entry."""
    async_add_entities(
        Solution3000ControlPanelEntity(
            coordinator=hass.data[DOMAIN][entry.entry_id]["panel_update"],
            entry_id=entry.entry_id,
            area=area,
        )
        for area in hass.data[DOMAIN][entry.entry_id]["panel_update"].data.areas
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
        self.check_code = False
        if self.coordinator.data.requires_pin:
            self._attr_code_format = alarm.CodeFormat.NUMBER
            self.check_code = True

    @property
    def state(self) -> str | None:
        """Return the state of the sensor."""
        if self.area.status in [AreaStatus.AllOn, AreaStatus.PartOnDelay, AreaStatus.PartOnInstant]:
            if AlarmMemoryPriorities.BurglaryAlarm in self.area.alarms:
                return STATE_ALARM_TRIGGERED
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
        if self.check_code and code != self.coordinator.data.pincode:
            return
        """Send disarm command."""
        await self.coordinator.data.arm(ArmType.Disarmed, [self.area])

    async def async_alarm_arm_away(self, code=None) -> None:
        if self.check_code and code != self.coordinator.data.pincode:
            return
        self.area.status = AreaStatus.AllOnExitDelay
        self.async_schedule_update_ha_state()
        await self.coordinator.data.arm(ArmType.Away, [self.area])

    async def async_alarm_arm_home(self, code=None) -> None:
        if self.check_code and code != self.coordinator.data.pincode:
            return
        self.area.status = AreaStatus.PartOnExitDelay
        self.async_schedule_update_ha_state()
        await self.coordinator.data.arm(ArmType.Stay, [self.area])

    async def async_alarm_arm_night(self, code=None) -> None:
        if self.check_code and code != self.coordinator.data.pincode:
            return
        self.area.status = AreaStatus.PartOnExitDelay
        self.async_schedule_update_ha_state()
        await self.coordinator.data.arm(ArmType.Stay2, [self.area])

    @property
    def extra_state_attributes(self):
        messages = self.coordinator.data.history_messages.copy()
        messages.reverse()
        if self.coordinator.data.history_count:
            messages = messages[:self.coordinator.data.history_count]
        return {"panel_history": "\n".join([f"{message.datetime} | {message.message}" for message in messages]), "area_alarms": "\n".join([x.name for x in self.area.alarms])}
