import socket
import ssl
from enum import Enum
import asyncio


class UserType(Enum):
    InstallerApp = 0x00
    AutomationUser = 0x01
    RemoteUser = 0x02


class Commands(Enum):
    WhatAreYou = 0x01
    TerminateSession = 0x05
    Passcode = 0x06
    ReqRawHistoryEvents = 0x15
    ReqTextHistoryEvents = 0x16
    ResetSensors = 0x18
    SilenceBells = 0x19
    ReqAlarmMemoryPriorities = 0x21
    ReqAlarmAreasByPriority = 0x22
    ReqConfiguredAreas = 0x24
    ReqPanelCapacitie = 0x1F
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
    ReqPointsInArea = 0x35
    ReqConfiguredPoints = 0x36
    ReqFaultedPoints = 0x37
    ReqPointStatus = 0x38
    ReqBypassedPoints = 0x39
    BypassPoints = 0x3A
    UnbypassPoints = 0x3B
    ReqPointText = 0x3C
    Pincode = 0x3E
    ReqUser = 0x40
    SetSubscriptions = 0x5F


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
    BadAccessCardData = 0XE5
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


class ProtocolVersion():
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


class Component():
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

    def __str__(self) -> str:
        return f"Area(id={self.id}, name={self.name}, status={self.status}, points={', '.join(map(Point.__str__, self.points))})"


class Panel():
    areas: list[Area]
    def __init__(self, port: int, ip: str, user_type: UserType, passcode: str, pincode: str) -> None:
        self.port = port
        self.ip = ip
        self.user_type = user_type
        self.passcode = passcode
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

    async def _send_packet(self, command: Commands, command_format: list[int] = None, data: list[int] | bytearray = None):
        command_format = command_format or []
        data = data or []
        if not isinstance(data, bytearray):
            data = bytearray(data)
        length = 1 + len(command_format) + len(data)
        protocol = 0x01
        packet = bytearray([protocol, length, command.value]
                           ) + bytearray(command_format) + data
        self.writer.write(packet)
        await self.writer.drain()

    async def _receive_packet(self, expected_response: int) -> bytes:
        protocol = (await self.reader.read(1))[0]
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

    async def _send_what_are_you(self):
        await self._send_packet(Commands.WhatAreYou, [])
        data = await self._receive_packet(0xFE)
        self.panel_type = PanelType(data[1])
        self.rps_protocol_version = ProtocolVersion(
            data[2], data[3], data[4] + 255 * data[5])
        self.intrusion_integration_protocol_version = ProtocolVersion(
            data[6], data[7], data[8] + 255 * data[9])
        self.execute_protocol_version = ProtocolVersion(
            data[10], data[11], data[12] + 255 * data[13])
        flags = data[14]
        if flags == MaxConnectionsInUseFlags.MaxUserBasedRemoteAccessUsersInUse:
            raise PanelException("Max User Based Remote Access Users In Use")
        if flags == MaxConnectionsInUseFlags.MaxAutomationUsersInUse:
            raise PanelException("Max Automation Users In Use")

    async def _authenticate(self):
        if len(self.passcode) > 24 or len(self.passcode) < 6:
            raise PanelException("Invalid Passcode Length")
        if len(self.passcode) < 24:
            self.passcode += " "
        self.passcode = "\x00"+self.passcode
        await self._send_packet(Commands.Passcode, [],
                         bytearray(self.passcode, 'utf-8'))
        data = await self._receive_packet(0xFE)
        if data[1] == 0:
            raise PanelException("Invalid App Passcode")
        if data[1] == 2:
            raise PanelException("Panel is busy")
        # Solution3000 requires another round of authentication
        if self.panel_type == PanelType.Solution3000:
            pincode_num = int(self.pincode, 16)
            pincode_low = pincode_num & 0xff
            pincode_high = (pincode_num >> 8) & 0xff
            await self._send_packet(Commands.Pincode, [], [pincode_high, pincode_low])
            await self._receive_packet(0xFE)

    async def _req_capacities(self):
        await self._send_packet(Commands.ReqPanelCapacitie)
        data = await self._receive_packet(0xFE)
        self.max_areas = (data[2] * 255) + data[3]
        self.max_points = (data[4] * 255) + data[5]
        self.max_outputs = (data[6] * 255) + data[7]
        self.max_users = (data[8] * 255) + data[9]
        self.max_keypads = data[10]
        self.max_doors = data[11]

    async def _req_data_with_text(self, read_type: Commands, read_type_data: list[int], read_name: Commands, max: int):
        out = []
        if max:
            await self._send_packet(read_type, [], read_type_data)
            data = await self._receive_packet(0xFE)
            mask = 0
            for i in range(len(data) - 1):
                mask = mask << 8 | data[i + 1]
            max_bytes = (max + 8 - 1) // 8 * 8
            for id in range(max):
                if mask & (1 << (max_bytes-1-id)):
                    high = ((id + 1) >> 8) & 0xFF
                    low = (id + 1) & 0xFF
                    await self._send_packet(read_name, [], [high, low, 0, 1])
                    data = await self._receive_packet(0xFE)
                    length = data[1]
                    name = data[1:length].decode("utf-8")
                    out.append((id+1, name))
        return out

    async def _req_data_status(self, status_command: Commands, status_command_data: list[int], data_container, enumeration: Enum | None):
        if len(data_container):
            packet_data = status_command_data or []
            dataById = {}
            for data in data_container:
                packet_data.extend([0, data.id])
                dataById[data.id] = data
            await self._send_packet(status_command, [], packet_data)
            response = await self._receive_packet(0xFE)
            response = response[1:]
            while response:
                id = response[1]
                status = response[2]
                if enumeration:
                    dataById[id].status = enumeration(status)
                else:
                    dataById[id].status = status
                response = response[3:]

    async def _req_areas(self):
        self.areas = []
        area_data = await self._req_data_with_text(
            Commands.ReqConfiguredAreas, [], Commands.ReqAreaText, self.max_areas)
        for area_id, area_name in area_data:
            points = list(map(lambda data: Point(data[0], data[1]), await self._req_data_with_text(
                Commands.ReqPointsInArea, [0, area_id], Commands.ReqPointText, self.max_points)))
            self.areas.append(Area(area_id, area_name, points))

        output_data = await self._req_data_with_text(
            Commands.ReqConfiguredOutputs, [], Commands.ReqOutputText, self.max_areas)
        self.outputs = list(map(lambda x: Output(x[0], x[1]), output_data))

        door_data = await self._req_data_with_text(
            Commands.ReqConfiguredDoors, [], Commands.ReqDoorText, self.max_doors)
        self.doors = list(map(lambda x: Door(x[0], x[1]), door_data))


    async def arm(self, arm_type: ArmType, area: list[Area]):
        await self._send_packet(Commands.ArmPanelAreas, [], [arm_type.value, 0x80])

    async def update_status(self):
        await self._req_data_status(Commands.ReqAreaStatus,
                             [], self.areas, AreaStatus)
        for area in self.areas:
            await self._req_data_status(Commands.ReqPointStatus,
                                 [], area.points, PointStatus)
        await self._req_data_status(Commands.ReqDoorStatus, [], self.doors, None)
        await self._req_data_status(Commands.ReqOutputStatus, [],
                                   self.outputs, OutputStatus)
    async def initialise(self):
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.set_ciphers('DEFAULT')
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        self.reader, self.writer = await asyncio.open_connection(self.ip, self.port, ssl=context)
        await self._send_what_are_you()
        await self._authenticate()
        await self._req_capacities()
        await self._req_areas()

    def close(self):
        self.writer.close()

    def __del__(self):
        self.close()

    def __str__(self) -> str:
        return f"Panel(ip={self.ip}, port={self.port}, type={self.panel_type.name}, rps_protocol_version={self.rps_protocol_version}, \
intrusion_integration_protocol_version={self.intrusion_integration_protocol_version}, execute_protocol_version={self.execute_protocol_version}, \
max_areas={self.max_areas}, max_points={self.max_points}, max_users={self.max_users}, max_keypads={self.max_keypads}, max_doors={self.max_doors}, \
areas=[{', '.join(map(Area.__str__, self.areas))}]), \
doors=[{', '.join(map(Door.__str__, self.doors))}]), \
outputs=[{', '.join(map(Output.__str__, self.outputs))}])"