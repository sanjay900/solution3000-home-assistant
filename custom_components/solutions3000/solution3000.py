import socket
import ssl
from enum import Enum
import asyncio
from typing import Union
import struct
import datetime

from .bosch_history import parse_history_message

class UserType(Enum):
    InstallerApp = 0x00
    AutomationUser = 0x01
    RemoteUser = 0x02

class Commands(Enum):
    WhatAreYou = 0x01
    SetupEncryptionCommandCode = 0x02
    PublicKeyCommand = 0x03
    CheckEncryptionCommand = 0x04
    TerminateSession = 0x05
    Passcode = 0x06
    ReqPermissionForPanelAction = 0x07
    ReqAlarmMemorySummary = 0x08
    ReqAllowedAreasForAreaAction = 0x09
    ReqAllowedDoorsForDoorAction = 0x0a
    ReqPermissionForOutputAction = 0x0b
    ReqAllowedPointsForPointAction = 0x0c
    SetPanelTimeCommandCode = 0x11
    ReqPanelTimeCommandCode = 0x12
    ReqRawHistoryEvents = 0x15
    ReqTextHistoryEvents = 0x16
    ResetSensors = 0x18
    SilenceBells = 0x19
    ReqPanelCapacitie = 0x1F
    ReqAlarmMemoryPriorities = 0x21
    ReqAlarmAreasByPriority = 0x22
    ReqAlarmMemoryDetail = 0x23
    ReqConfiguredAreas = 0x24
    ReqAreaStatus = 0x26
    ArmPanelAreas = 0x27
    ReqAreaText = 0x29
    ReqConfiguredDoors = 0x2B
    ReqDoorStatus = 0x2C
    SetDoorState = 0x2D
    ReqDoorText = 0x2E
    ReqConfiguredOutputs = 0x30
    ReqOutputStatus = 0x31
    SetOutputState = 0x32
    ReqOutputText = 0x33
    ReqConfiguredPoints = 0x35
    ReqPointsInArea = 0x36
    ReqFaultedPoints = 0x37
    ReqPointStatus = 0x38
    ReqBypassedPoints = 0x39
    BypassPoints = 0x3A
    UnbypassPoints = 0x3B
    ReqPointText = 0x3C
    LoginUserCommandCode = 0x3E
    ReqUser = 0x40
    ReqCameraNamesCommandCode = 0x54
    ReqCameraLiveViewerDataCommand = 0x55
    ReqConfiguredCamerasCommandCode = 0x56
    SetSubscriptions = 0x5F
    UserBasedLoginCommandCode = 0x62
    GetRawHistoryEventsExtended = 0x63
    ReqBypassedPointsExt = 0x65
    ServiceBypassPointsCommand = 0x66
    ReqPanelLanguageCommandCode = 0xcc

class AlarmMemoryPriorities(Enum):
	Unknown = 0,
	Tamper = 11,
	FireAlarm = 10,
	GasAlarm = 9,
	PersonalEmergency = 8,
	BurglaryAlarm = 7,
	FireSupervisory = 6,
	FireTrouble = 5,
	GasSupervisory = 4,
	GasTrouble = 3,
	BurglarySupervisory = 2,
	BurglaryTrouble = 1

class PanelType(Enum):
    Undefined = 0x00
    Solution2000 = 0x20
    Solution3000 = 0x21
    AMAX2100 = 0x22
    AMAX3000 = 0x23
    AMAX4000 = 0x24
    D7412GV4 = 0x79
    D9412GV4 = 0x84
    B4512 = 0xAA0
    B5512 = 0xA4
    B8512G = 0xA6
    B9512G = 0xA7
    B3512 = 0xA8
    B6512 = 0xA9

class EventCategories(Enum):
    NoEvents = 0x00
    AlarmEvent = 0x01
    SystemEvent = 0x02
    ArmingEvent = 0x04
    DisabledEvent = 0x08
    AllEvents = 0x0F

PanelTypeNames = {
    PanelType.Undefined: "Undefined",
    PanelType.Solution2000: "Solution 2000",
    PanelType.Solution3000: "Solution 3000",
    PanelType.AMAX2100: "AMAX 2100",
    PanelType.AMAX3000: "AMAX 3000",
    PanelType.AMAX4000: "AMAX 4000",
    PanelType.D7412GV4: "D7412GV4",
    PanelType.D9412GV4: "D9412GV4",
    PanelType.B4512: "B4512",
    PanelType.B5512: "B5512",
    PanelType.B8512G: "B8512G",
    PanelType.B9512G: "B9512G",
    PanelType.B3512: "B3512",
    PanelType.B6512: "B6512",
}


class MaxConnectionsInUseFlags(Enum):
    MaxUserBasedRemoteAccessUsersInUse = 0x04
    MaxAutomationUsersInUse = 0x02
    MaxRPSAlinkusersInUse = 0x01


class NegativeAcknoledgement(Enum):
    NonSpecificError = 0x00
    ChecksumFailureUDPConnectionsOnly = 0x01
    InvalidSizeLength = 0x02
    InvalidCommand = 0x03
    InvalidInterfaceState = 0x04
    DataOutOfRange = 0x05
    Noauthority = 0x05
    Unsupportedcommand = 0x07
    CannotArmPanel = 0x08
    InvalidRemoteID = 0x09
    InvalidLicense = 0x0A
    InvalidMagicNumber = 0x0B
    ExpiredLicense = 0x0C
    ExpiredMagicNumber = 0x0D
    UnsupportedFormatVersion = 0x0E
    FirmwareUpdateInProgress = 0x11
    IncompatibleFirmwareVersion = 0x12
    AllPointsNotConfigured = 0x12
    ExecutionFunctionNoErrors = 0x20
    ExecutionFunctionInvalidArea = 0x21
    ExecutionFunctionInvalidCommand = 0x22
    ExecutionFunctionNotAuthenticated = 0x23
    ExecutionFunctionInvalidUser = 0x24
    ExecutionFunctionParameterIncorrect = 0x40
    ExecutionFunctionSequenceWrong = 0x41
    ExecutionFunctionInvalidConfigurationRequest = 0x42
    ExecutionFunctionInvalidSize = 0x43
    ExecutionFunctionTimeOut = 0x44
    RFRequestFailed = 0xDF
    NoRFdevicewiththatRFID = 0xE0
    BadRFIDNotProperFormat = 0xE1
    TooManyRFFevicesForThisPanel = 0xE2
    DuplicateRFID = 0xE3
    DuplicateAccessCard = 0xE4
    BadAccessCardData = 0xE5
    BadLanguageChoice = 0xE6
    BadSupervisionModeSelection = 0xE7
    BadEnableDisableChoice = 0xE8
    BadMonth = 0xE9
    BadDay = 0xEA
    BadHour = 0xEB
    BadMinute = 0xEC
    BadTimeEditChoice = 0xED
    BadRemoteEnable = 0xEF


class ArmType(Enum):
    Disarmed = 0x01
    Stay = 0x0A
    Stay2 = 0x0B
    Away = 0x0C


class DoorState(Enum):
    NoAction = 0x00
    Cycle = 0x01
    UnlockDoor = 0x02
    TerminateUnlockMode = 0x03
    Secure = 0x04
    TerminateSecureMode = 0x05


class AreaStatus(Enum):
    Unknown = 0x00
    AllOn = 0x01
    PartOnInstant = 0x02
    PartOnDelay = 0x03
    Disarmed = 0x04
    AllOnEntryDelay = 0x05
    PartOnEntryDelay = 0x06
    AllOnExitDelay = 0x07
    PartOnExitDelay = 0x08
    AllOnInstantArmed = 0x09


class PointStatus(Enum):
    Unassigned = 0x00
    Short = 0x01
    Open = 0x02
    Normal = 0x03
    Missing = 0x04


class OutputStatus(Enum):
    Inactive = 0x00
    Active = 0x01
    Unknown = 0x02


class ProtocolVersion:
    def __init__(self, major, minor, revision) -> None:
        self.major = major
        self.minor = minor
        self.revision = revision

    def __str__(self) -> str:
        return f"Version({self.major}.{self.minor}.{self.revision})"


class PanelException(Exception):
    def __init__(self, *args: object) -> None:
        if isinstance(args[0], NegativeAcknoledgement):
            super().__init__(f"Bosch Panel Error {args[0].name}")
            return
        super().__init__(*args)


class Component:
    def __init__(self, id, name, status) -> None:
        self.id = id
        self.name = name
        self.status = status


class Point(Component):
    def __init__(self, id, name) -> None:
        super().__init__(id, name, PointStatus.Unassigned)

    def __str__(self) -> str:
        return f"Point(id={self.id}, status={self.status}, name={self.name})"


class DoorMasks(Enum):
    Unlocked = 1 << 7
    Secured = 1 << 6
    InLearnMode = 1 << 5
    InDiagnosticMode = 1 << 4
    InSDIFailureMode = 1 << 2
    Unknown = 0


class Door(Component):
    def __init__(self, id, name) -> None:
        super().__init__(id, name, DoorMasks.Unknown)

    def is_locked(self):
        return not (self.status & DoorMasks.Unlocked)

    def is_secured(self):
        return self.status & DoorMasks.Secured

    def is_in_learn_mode(self):
        return self.status & DoorMasks.InLearnMode

    def is_in_diagnostic_mode(self):
        return self.status & DoorMasks.InDiagnosticMode

    def is_in_SDI_failure_mode(self):
        return self.status & DoorMasks.InSDIFailureMode

    def __str__(self) -> str:
        return f"Door(id={self.id}, name={self.name}, locked={self.is_locked()}, secured={self.is_secured()}, in_learn_mode={self.is_in_learn_mode()}, in_diagnostic_mode={self.is_in_diagnostic_mode()}, in_SDI_failure_mode={self.is_in_SDI_failure_mode()})"


class Output(Component):
    def __init__(self, id, name) -> None:
        super().__init__(id, name, OutputStatus.Unknown)

    def __str__(self) -> str:
        return f"Output(id={self.id}, name={self.name}, status={self.status})"


class Area(Component):
    def __init__(self, id, name, points: list[Point]) -> None:
        super().__init__(id, name, AreaStatus.Unknown)
        self.points = points
        self.alarms = []

    def __str__(self) -> str:
        return f"Area(id={self.id}, name={self.name}, status={self.status}, points={', '.join(map(Point.__str__, self.points))}), alarms={', '.join(map(AlarmMemoryPriorities.__str__, self.alarms))})"

class HistoryMessage():
    def __init__(self, datetime, message, event_code, first_param, second_param) -> None:
        self.datetime = datetime
        self.message = message
        self.event_code = event_code
        self.first_param = first_param
        self.second_param = second_param
        
    def __str__(self) -> str:
        return f"HistoryMessage(datetime={self.datetime}, message={self.message}, event_code={self.event_code})"

class Panel:
    areas: list[Area]

    def __init__(
        self, port: int, ip: str, pincode: str, show_history: bool, history_count: int
    ) -> None:
        self.show_history = show_history
        self.history_count = history_count
        self.port = port
        self.ip = ip
        self.pincode = pincode
        self.panel_type = PanelType.Undefined
        self.rps_protocol_version = ProtocolVersion(0, 0, 0)
        self.intrusion_integration_protocol_version = ProtocolVersion(0, 0, 0)
        self.execute_protocol_version = ProtocolVersion(0, 0, 0)
        self.max_areas = 0
        self.max_points = 0
        self.max_outputs = 0
        self.max_users = 0
        self.max_keypads = 0
        self.max_doors = 0
        self.areas = []
        self.outputs = []
        self.doors = []
        self.lock = asyncio.Lock()
        self.last_history_message = 0
        self.history_messages = []
        self.writer = None

    async def _xfer_packet(
        self,
        command: Commands,
        expected_response: int,
        command_format: list[int] = None,
        data: Union[list[int], bytearray] = None,
    ):
        try:
            async with self.lock:
                command_format = command_format or []
                data = data or []
                if not isinstance(data, bytearray):
                    data = bytearray(data)
                length = 1 + len(command_format) + len(data)
                protocol = 0x01
                packet = (
                    bytearray([protocol, length, command.value])
                    + bytearray(command_format)
                    + data
                )
                self.writer.write(packet)
                await self.writer.drain()
                data = await self.reader.read(1)
                if not data:
                    raise ConnectionError()
                protocol = data[0]
                if protocol == 1:
                    length = (await self.reader.read(1))[0]
                    data = await self.reader.read(length)
                    if data[0] != expected_response:
                        if data[0] == 0xFD:
                            raise PanelException(NegativeAcknoledgement(data[1]))
                        else:
                            raise PanelException(f"Unknown error {data}")
                    return data
                else:
                    raise PanelException(f"Unexpected protocol {protocol}")
        except ConnectionError:
            await self.close()
            await self.initialise()
            return await self._xfer_packet(command, expected_response, command_format, data)


    def panel_type_name(self):
        return PanelTypeNames[self.panel_type]

    async def _send_what_are_you(self):
        data = await self._xfer_packet(Commands.WhatAreYou, 0xFE, [])
        self.panel_type = PanelType(data[1])
        self.rps_protocol_version = ProtocolVersion(
            data[2], data[3], data[4] + 255 * data[5]
        )
        self.intrusion_integration_protocol_version = ProtocolVersion(
            data[6], data[7], data[8] + 255 * data[9]
        )
        self.execute_protocol_version = ProtocolVersion(
            data[10], data[11], data[12] + 255 * data[13]
        )
        flags = data[14]
        if flags == MaxConnectionsInUseFlags.MaxUserBasedRemoteAccessUsersInUse:
            raise PanelException("Max User Based Remote Access Users In Use")
        if flags == MaxConnectionsInUseFlags.MaxAutomationUsersInUse:
            raise PanelException("Max Automation Users In Use")

    async def _authenticate(self):
        # Solution2000 / 3000 uses a a-link pin code, the others use a automation passcode
        if self.panel_type == PanelType.Solution3000 or self.panel_type == PanelType.Solution2000:
            pincode_num = int(str(self.pincode), 16)
            pincode_low = pincode_num & 0xFF
            pincode_high = (pincode_num >> 8) & 0xFF
            try:
                await self._xfer_packet(Commands.LoginUserCommandCode, 0xFE, [], [pincode_high, pincode_low])
            except PanelException as e:
                if e.args[0] == "Bosch Panel Error NonSpecificError":
                    raise PanelException("Error authenticating with alink code, is it correct?")
                raise e
        else:
            if len(self.pincode) > 24 or len(self.pincode) < 6:
                raise PanelException("Invalid Passcode Length")
            if len(self.pincode) < 24:
                self.pincode += " "
            self.pincode = "\x00" + self.pincode
            data = await self._xfer_packet(
                Commands.Passcode, 0xFE, [], bytearray(self.pincode, "utf-8")
            )
            if data[1] == 0:
                raise PanelException("Error authenticating with automation code, is it correct?")
            if data[1] == 2:
                raise PanelException("Panel is busy")
    async def _req_history(self):
        try:
        # We get data chunked, so just read until we run out of data.
            while True:
                data = await self._xfer_packet(Commands.GetRawHistoryEventsExtended, 0xFE, [0xff],struct.pack(">i",self.last_history_message))
                if len(data) <= 6:
                    break
                data = data[6:]
                count = len(data) // 8
                for i in range(count):
                    start = i*8
                    end = start + 8
                    section = data[start:end]
                    year = 2000 + ((section[3] & 0xFC) >> 2)
                    month = ((section[3] & 3) << 2) | ((section[2] & 0xC0) >> 6)
                    day = (section[1] & 0xF8) >> 3
                    hour = ((section[1] & 7) << 2) | ((section[0] & 0xC0) >> 6)
                    minute = section[0] & 0x3F
                    second = section[2] & 0x3F
                    first_param=section[5] * 256 + section[4]
                    second_param=section[7]
                    event_code=section[6]
                    date = datetime.datetime(year,month,day,hour,minute,second)
                    self.history_messages.append(HistoryMessage(date, parse_history_message(event_code, first_param, second_param, self.panel_type.name), event_code, first_param, second_param))
                self.last_history_message += count
        except PanelException as e:
            # If we get a NonSpecificError while reading history it just means that the history data is currently being updated.
            if not e.args[0] == "Bosch Panel Error NonSpecificError":
                raise e

    async def _req_capacities(self):
        data = await self._xfer_packet(Commands.ReqPanelCapacitie, 0xFE)
        self.max_areas = (data[2] * 255) + data[3]
        self.max_points = (data[4] * 255) + data[5]
        self.max_outputs = (data[6] * 255) + data[7]
        self.max_users = (data[8] * 255) + data[9]
        self.max_keypads = data[10]
        self.max_doors = data[11]

    async def _req_data_with_text(
        self,
        read_type: Commands,
        read_type_data: list[int],
        read_name: Commands,
        max: int,
    ):
        out = []
        if max:
            data = await self._xfer_packet(read_type, 0xFE, [], read_type_data)
            mask = 0
            max_bits = 0
            for i in range(len(data) - 1):
                mask = mask << 8 | data[i + 1]
                max_bits += 8
            for id in range(max):
                if mask & (1 << (max_bits - 1 - id)):
                    high = ((id + 1) >> 8) & 0xFF
                    low = (id + 1) & 0xFF
                    data = await self._xfer_packet(read_name, 0xFE, [], [high, low, 0, 1])
                    length = data[1]
                    name = data[1:length].decode("utf-8")
                    out.append((id + 1, name))
        return out

    async def _req_area_status(
        self,
    ):

        packet_data = [2]
        area_by_id = {}
        for area in self.areas:
            packet_data.extend([0, area.id])
            area_by_id[area.id] = area
        response = await self._xfer_packet(Commands.ReqAreaStatus, 0xFE, [], packet_data)
        response = response[1:]
        while response:
            data_id = response[1]
            status = response[2]
            area_by_id[data_id].status = AreaStatus(status)
            alarms = []
            if ((response[3] & 2) == 2):
                alarms.append(AlarmMemoryPriorities.FireAlarm)
            if ((response[3] & 1) == 1):
                alarms.append(AlarmMemoryPriorities.GasAlarm)
            if ((response[4] & 0x80) == 128):
                alarms.append(AlarmMemoryPriorities.PersonalEmergency)
            if ((response[4] & 0x40) == 64):
                alarms.append(AlarmMemoryPriorities.BurglaryAlarm)
            if ((response[4] & 0x20) == 32):
                alarms.append(AlarmMemoryPriorities.FireSupervisory)
            if ((response[4] & 0x10) == 16):
                alarms.append(AlarmMemoryPriorities.FireTrouble)
            if ((response[4] & 8) == 8):
                alarms.append(AlarmMemoryPriorities.GasSupervisory)
            if ((response[4] & 4) == 4):
                alarms.append(AlarmMemoryPriorities.GasTrouble)
            if ((response[4] & 2) == 2):
                alarms.append(AlarmMemoryPriorities.BurglarySupervisory)
            if ((response[4] & 1) == 1):
                alarms.append(AlarmMemoryPriorities.BurglaryTrouble)

            area_by_id[data_id].alarms = alarms
            response = response[6:]

    async def _req_data_status(
        self,
        status_command: Commands,
        status_command_data: list[int],
        data_container,
        enumeration: Union[Enum, None],
    ):
        if len(data_container):
            packet_data = status_command_data or []
            data_by_id = {}
            for data in data_container:
                packet_data.extend([0, data.id])
                data_by_id[data.id] = data
            response = await self._xfer_packet(status_command, 0xFE, [], packet_data)
            response = response[1:]
            while response:
                data_id = response[1]
                status = response[2]
                if enumeration:
                    data_by_id[data_id].status = enumeration(status)
                else:
                    data_by_id[data_id].status = status
                response = response[3:]

    async def _req_areas(self):
        self.areas = []
        area_data = await self._req_data_with_text(
            Commands.ReqConfiguredAreas, [], Commands.ReqAreaText, self.max_areas
        )
        for area_id, area_name in area_data:
            points = list(
                map(
                    lambda data: Point(data[0], data[1]),
                    await self._req_data_with_text(
                        Commands.ReqPointsInArea,
                        [0, area_id],
                        Commands.ReqPointText,
                        self.max_points,
                    ),
                )
            )
            self.areas.append(Area(area_id, area_name, points))

        output_data = await self._req_data_with_text(
            Commands.ReqConfiguredOutputs, [], Commands.ReqOutputText, self.max_areas
        )
        self.outputs = list(map(lambda x: Output(x[0], x[1]), output_data))

        door_data = await self._req_data_with_text(
            Commands.ReqConfiguredDoors, [], Commands.ReqDoorText, self.max_doors
        )
        self.doors = list(map(lambda x: Door(x[0], x[1]), door_data))

    async def arm(self, arm_type: ArmType, areas: list[Area]):
        mask = 0
        for area in areas:
            mask |= 1 << (8-area.id)
            if arm_type == ArmType.Away:
                area.status = AreaStatus.AllOnExitDelay
            if arm_type == ArmType.Stay or arm_type == ArmType.Stay2:
                area.status = AreaStatus.PartOnExitDelay
        await self._xfer_packet(Commands.ArmPanelAreas, 0xFC, [], [arm_type.value, mask])

    async def set_output(self, output: Output, state: OutputStatus):
        output.status = state
        await self._xfer_packet(Commands.SetOutputState, 0xFC, [], [output.id, state])

    async def set_door(self, door: Door, state: int):
        door.status = state
        await self._xfer_packet(Commands.SetDoorState, 0xFC, [], [door.id, state])

    async def update_status(self):
        await self._req_area_status()
        for area in self.areas:
            await self._req_data_status(
                Commands.ReqPointStatus, [], area.points, PointStatus
            )
        await self._req_data_status(Commands.ReqDoorStatus, [], self.doors, None)
        await self._req_data_status(
            Commands.ReqOutputStatus, [], self.outputs, OutputStatus
        )
        if self.show_history:
            await self._req_history()
        return self

    async def initialise(self):
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.set_ciphers("DEFAULT")
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        self.reader, self.writer = await asyncio.open_connection(
            self.ip, self.port, ssl=context
        )
        await self._send_what_are_you()
        await self._authenticate()
        await self._req_capacities()
        await self._req_areas()

    async def close(self):
        async with self.lock:
            if self.writer:
                self.writer.close()

    def __del__(self):
            if self.writer:
                self.writer.close()

    def __str__(self) -> str:
        return f"Panel(ip={self.ip}, port={self.port}, type={self.panel_type.name}, rps_protocol_version={self.rps_protocol_version}, \
intrusion_integration_protocol_version={self.intrusion_integration_protocol_version}, execute_protocol_version={self.execute_protocol_version}, \
max_areas={self.max_areas}, max_points={self.max_points}, max_users={self.max_users}, max_keypads={self.max_keypads}, max_doors={self.max_doors}, \
areas=[{', '.join(map(Area.__str__, self.areas))}]), \
doors=[{', '.join(map(Door.__str__, self.doors))}]), \
outputs=[{', '.join(map(Output.__str__, self.outputs))}]), history=[{', '.join(map(HistoryMessage.__str__, self.history_messages))}])"
