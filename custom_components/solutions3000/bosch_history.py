def solutions_key(first_param):
        if first_param >= 1 and first_param <= 32:
            return "_User"
        match first_param:
            case 0:
                return "_Quick"
            case 994:
                return "_PowerUp"
            case 995:
                return "_Telephone"
            case 997:
                return "_Schedule"
            case 998:
                return "_ALink"
            case 999:
                return "_Installer"
        return ""
def amax_conflict_source_key(first_param):
    if first_param >= 1 and first_param <= 64:
        return "_RfZone"
    if first_param >= 65 and first_param <= 72:
        return "_RfRepeater"
    if first_param >= 256 and first_param <= 506:
        return "_User"
    return "_Unknown"
def amax_tamper_key(first_param):
    if first_param >= 1 and first_param <= 16:
        return "_Keypad"
    if first_param == 0:
        return "_OnboardTamper"
    if first_param >= 102 and first_param <= 108:
        return "_InputModule"
    return "_Unknown"
def amax_module_key(first_param):
    if first_param >= 1 and first_param <= 16:
        return "_Keypad"
    if first_param >= 102 and first_param <= 108:
        return "_InputModule"
    if first_param >= 150 and first_param <= 151:
        return "_RelayOutputModule"
    if first_param == 134 or first_param == 250:
        return "_IpModule"
    return "_Unknown"
def amax_arming_key(first_param):
    match first_param:
        case 0:
            return "_Installer"
        case 251:
            return "_RPC"
        case 252:
            return "_Remote"
        case 253:
            return "_QuickArm"
        case 254:
            return "_KeySwitch"
        case _:
            return "_User"
def parse_history_message(eventCode, first_param, second_param, panel_type_name):
    eventType = "99"
    if "AMAX" in panel_type_name:
        eventType = "00"
    if "Solution" in panel_type_name:
        eventType = "01"
    key = f"{eventType}_{str(eventCode).rjust(4,'0')}"
    text = "Unknown History Event"
    if eventType == "00":
        match eventCode:
            case 26:
                if first_param == 0:
                    key += "_Auto"
                else:
                    key += "_Manual"
            case 62 | 63 | 105 | 106 | 107 | 108 | 109:
                if first_param == 134:
                    key += "_MODULE1"
                elif first_param == 250:
                    key += "_MODULE2"
            case 30 | 31:
                key += amax_module_key(first_param)
            case 32 | 33:
                key += amax_tamper_key(first_param)
    if eventType == "01":
        if eventCode >= 47 and eventCode <= 60:
            if eventCode <= 50 or eventCode >= 54:
                key += solutions_key(first_param)
            if second_param == 0:
                key += "_NoArea"
        if eventCode == 110:
            if first_param == 998:
                key += "_ALink"
            else:
                key += "_User"
    match key:
        case "00_0000":
            text = f"System reset"
        case "00_0001":
            text = f"Area {second_param}, zone {first_param} burglary alarm"
        case "00_0002":
            text = f"Area {second_param}, zone {first_param} burglary alarm restore"
        case "00_0003":
            text = f"Area {second_param}, zone {first_param} 24 hour burglary alarm"
        case "00_0004":
            text = f"Area {second_param}, zone {first_param} 24 hour burglary alarm restore"
        case "00_0005":
            text = f"Area {second_param}, zone {first_param} burglary trouble"
        case "00_0006":
            text = f"Area {second_param}, zone {first_param} burglary trouble restore"
        case "00_0007":
            text = f"Area {second_param}, zone {first_param} burglary bypass"
        case "00_0008":
            text = f"Area {second_param}, zone {first_param} burglary bypass restore"
        case "00_0009":
            text = f"Area {second_param}, zone {first_param} Tamper alarm"
        case "00_0010":
            text = f"Area {second_param}, zone {first_param} Tamper restore"
        case "00_0011_Installer":
            text = f"Area {first_param} arm by installer (AWAY)"
        case "00_0011_KeySwitch":
            text = f"Area {first_param} arm by key switch (AWAY)"
        case "00_0011_QuickArm":
            text = f"Area {first_param} arm by quick arm (AWAY)"
        case "00_0011_RPC":
            text = f"Area {first_param} arm by RPC (AWAY)"
        case "00_0011_Remote":
            text = f"Area {first_param} arm by remote(AWAY)"
        case "00_0011_User":
            text = f"Area {second_param} arm by user {first_param} (AWAY)"
        case "00_0012_Installer":
            text = f"Area {first_param} disarm by installer(AWAY)"
        case "00_0012_KeySwitch":
            text = f"Area {first_param} disarm by key switch (AWAY)"
        case "00_0012_RPC":
            text = f"Area {first_param} disarm by RPC (AWAY)"
        case "00_0012_User":
            text = f"Area {second_param} disarm by user {first_param} (AWAY)"
        case "00_0013_Installer":
            text = f"Area {first_param} arm by installer (STAY)"
        case "00_0013_KeySwitch":
            text = f"Area {first_param} arm by key switch (STAY)"
        case "00_0013_QuickArm":
            text = f"Area {first_param} arm by quick arm (STAY)"
        case "00_0013_RPC":
            text = f"Area {first_param} arm by RPC (STAY)"
        case "00_0013_User":
            text = f"Area {second_param} arm by user {first_param} (STAY)"
        case "00_0014_Installer":
            text = f"Area {first_param} disarm by installer(STAY)"
        case "00_0014_KeySwitch":
            text = f"Area {first_param} disarm by key switch (STAY)"
        case "00_0014_RPC":
            text = f"Area {first_param} disarm by RPC (STAY)"
        case "00_0014_User":
            text = f"Area {second_param} disarm by user {first_param} (STAY)"
        case "00_0015":
            text = f"Keypad emergency"
        case "00_0016":
            text = f"Keypad fire"
        case "00_0017":
            text = f"Keypad medical"
        case "00_0018":
            text = f"Duress by user {first_param}"
        case "00_0019":
            text = f"Keypad no.# {first_param} lockout"
        case "00_0020":
            text = f"Low battery"
        case "00_0021":
            text = f"Battery restore"
        case "00_0022":
            text = f"AC fail"
        case "00_0023":
            text = f"AC restore"
        case "00_0024":
            text = f"AUX power fail {first_param}"
        case "00_0025":
            text = f"AUX power restore {first_param}"
        case "00_0026_Auto":
            text = f"Communication test"
        case "00_0026_Manual":
            text = f"Communication test"
        case "00_0027":
            text = f"Configuration change"
        case "00_0028":
            text = f"Communications destination {first_param} trouble"
        case "00_0029":
            text = f"Communications destination {first_param} trouble restore"
        case "00_0030_InputModule":
            text = f"DX2010-CHI trouble {first_param}"
        case "00_0030_IpModule":
            text = f"B420-CN/DX4020-G trouble {first_param}"
        case "00_0030_Keypad":
            text = f"Keypad trouble {first_param}"
        case "00_0030_RelayOutputModule":
            text = f"DX3010 trouble {first_param}"
        case "00_0031_InputModule":
            text = f"DX2010-CHI trouble restore {first_param}"
        case "00_0031_IpModule":
            text = f"B420-CN/DX4020-G trouble restore {first_param}"
        case "00_0031_Keypad":
            text = f"Keypad trouble restore {first_param}"
        case "00_0031_RelayOutputModule":
            text = f"DX3010 trouble restore {first_param}"
        case "00_0032_InputModule":
            text = f"DX2010-CHI tamper {first_param}"
        case "00_0032_Keypad":
            text = f"Keypad tamper"
        case "00_0032_OnboardTamper":
            text = f"Onboard tamper"
        case "00_0033_InputModule":
            text = f"DX2010-CHI tamper restore {first_param}"
        case "00_0033_Keypad":
            text = f"Keypad tamper restore"
        case "00_0033_OnboardTamper":
            text = f"Onboard tamper restore"
        case "00_0034":
            text = f"Date/time setting"
        case "00_0035":
            text = f"User code {first_param} change"
        case "00_0036":
            text = f"Enter program mode"
        case "00_0037":
            text = f"Exit program mode"
        case "00_0038":
            text = f"Phone line fail"
        case "00_0039":
            text = f"Phone line restore"
        case "00_0040":
            text = f"Area {second_param}, zone {first_param} 24 hour panic alarm"
        case "00_0041":
            text = f"Area {second_param}, zone {first_param} 24 hour panic alarm restore"
        case "00_0042":
            text = f"Area {second_param}, zone {first_param} 24 hour fire"
        case "00_0043":
            text = f"Area {second_param}, zone {first_param} 24 hour fire restore"
        case "00_0044":
            text = f"Area {second_param}, zone {first_param} fire unverified"
        case "00_0045":
            text = f"{first_param} Output fault"
        case "00_0046":
            text = f"{first_param} Output fault restore"
        case "00_0047":
            text = f"Summer time"
        case "00_0048":
            text = f"Winter time"
        case "00_0049":
            text = f"Fault override"
        case "00_0050":
            text = f"Panel access"
        case "00_0051":
            text = f"Software update"
        case "00_0052":
            text = f"Remote link success"
        case "00_0053":
            text = f"Clock fail"
        case "00_0054":
            text = f"Area {second_param}, zone {first_param} tamper alarm"
        case "00_0055":
            text = f"Area {second_param}, zone {first_param} tamper restore"
        case "00_0056":
            text = f"Area {second_param}, zone {first_param} zone EXT fault"
        case "00_0057":
            text = f"Area {second_param}, zone {first_param} zone EXT fault restore"
        case "00_0058":
            text = f"Area {second_param}, zone {first_param} exit delay"
        case "00_0059":
            text = f"Area {second_param}, zone {first_param} exit delay restore"
        case "00_0060":
            text = f"Area {second_param}, zone {first_param} burglary alarm verified"
        case "00_0061":
            text = f"Area {second_param}, zone {first_param} burglary alarm unverified"
        case "00_0062_MODULE1":
            text = f"IP module trouble #1"
        case "00_0062_MODULE2":
            text = f"IP module trouble #2"
        case "00_0063_MODULE1":
            text = f"IP module restore #1"
        case "00_0063_MODULE2":
            text = f"IP module restore #2"
        case "00_0064":
            text = f"Printer missing"
        case "00_0065":
            text = f"Printer missing restore"
        case "00_0066":
            text = f"Printer error"
        case "00_0067":
            text = f"Printer error restore"
        case "00_0068":
            text = f"Expansion device missing"
        case "00_0069":
            text = f"Expansion device missing restore"
        case "00_0070":
            text = f"Expansion missing"
        case "00_0071":
            text = f"Expansion missing restore"
        case "00_0072":
            text = f"Expansion device tamper"
        case "00_0073":
            text = f"Expansion tamper restore"
        case "00_0074":
            text = f"Expansion trouble"
        case "00_0075":
            text = f"Expansion trouble restore"
        case "00_0076":
            text = f"Wireless receiver jam"
        case "00_0077":
            text = f"Wireless receiver jam restore"
        case "00_0078_RfRepeater":
            text = f"Area {second_param} wireless zone {first_param} receiver config conflict"
        case "00_0078_RfZone":
            text = f"Area {second_param} wireless zone {first_param} receiver config conflict"
        case "00_0078_User":
            text = f"Area {second_param} wireless zone {first_param} receiver config conflict"
        case "00_0079_RfRepeater":
            text = f"Area {second_param} wireless zone {first_param} receiver config conflict restore"
        case "00_0079_RfZone":
            text = f"Area {second_param} wireless zone {first_param} receiver config conflict restore"
        case "00_0079_User":
            text = f"Area {second_param} wireless zone {first_param} receiver config conflict restore"
        case "00_0080":
            text = f"Area {second_param} wireless zone {first_param} missing"
        case "00_0081":
            text = f"Area {second_param} wireless zone {first_param} missing restore"
        case "00_0082":
            text = f"Area {second_param} wireless zone {first_param} low battery"
        case "00_0083":
            text = f"Area {second_param} wireless zone {first_param} low battery restore"
        case "00_0084":
            text = f"Area {second_param} wireless zone {first_param} trouble"
        case "00_0085":
            text = f"Area {second_param} wireless zone {first_param} trouble restore"
        case "00_0086":
            text = f"Wireless repeater {first_param} missing"
        case "00_0087":
            text = f"Wireless repeater {first_param} missing restore"
        case "00_0088":
            text = f"Wireless repeater {first_param} low battery"
        case "00_0089":
            text = f"Wireless repeater {first_param} low battery restore"
        case "00_0090":
            text = f"Wireless repeater {first_param} tamper"
        case "00_0091":
            text = f"Wireless repeater {first_param} tamper restore"
        case "00_0092":
            text = f"Wireless repeater {first_param} AC fail"
        case "00_0093":
            text = f"Wireless repeater {first_param} AC fail restore"
        case "00_0094":
            text = f"Wireless keyfob {first_param} low battery"
        case "00_0095":
            text = f"Wireless keyfob {first_param} low battery restore"
        case "00_0096":
            text = f"Wireless keyfob {first_param} panic alarm"
        case "00_0097":
            text = f"Wireless keyfob {first_param} silent alarm"
        case "00_0098":
            text = f"Wireless change keyfob {first_param}"
        case "00_0099":
            text = f"Area {second_param} wireless zone {first_param} enclosure tamper"
        case "00_0100":
            text = f"Area {second_param} wireless zone {first_param} enclosure tamper restore"
        case "00_0101":
            text = f"Area {second_param} wireless zone {first_param} missing"
        case "00_0102":
            text = f"Area {second_param} wireless zone {first_param} restore"
        case "00_0103":
            text = f"Service mode on"
        case "00_0104":
            text = f"Service mode off"
        case "00_0105_MODULE1":
            text = f"Network config changed #1"
        case "00_0105_MODULE2":
            text = f"Network config changed #2"
        case "00_0106_MODULE1":
            text = f"Network trouble #1"
        case "00_0106_MODULE2":
            text = f"Network trouble #2"
        case "00_0107_MODULE1":
            text = f"Network restore #1"
        case "00_0107_MODULE2":
            text = f"Network restore #2"
        case "00_0108_MODULE1":
            text = f"Push fail #1"
        case "00_0108_MODULE2":
            text = f"Push fail #2"
        case "00_0109_MODULE1":
            text = f"Push restore #1"
        case "00_0109_MODULE2":
            text = f"Push restore #2"
        case "01_0000":
            text = f"System reset"
        case "01_0001":
            text = f"Z{first_param} Alarm"
        case "01_0002":
            text = f"Z{first_param} Alarm Restore"
        case "01_0003":
            text = f"Z{first_param} Trouble"
        case "01_0004":
            text = f"Z{first_param} Trouble Restore"
        case "01_0005":
            text = f"Z{first_param} Bypass"
        case "01_0006":
            text = f"Z{first_param} UnBypass"
        case "01_0007":
            text = f"24Hr Z{first_param} Alarm"
        case "01_0008":
            text = f"24Hr Z{first_param} Alarm Restore"
        case "01_0009":
            text = f"24Hr Z{first_param} Trouble"
        case "01_0010":
            text = f"24Hr Z{first_param} Trouble Restore"
        case "01_0011":
            text = f"24Hr Z{first_param} Bypass"
        case "01_0012":
            text = f"24Hr Z{first_param} UnBypass"
        case "01_0013":
            text = f"24Hr Medical Z{first_param} Alarm"
        case "01_0014":
            text = f"24Hr Medical Z{first_param} Alarm Restore"
        case "01_0015":
            text = f"24Hr Medical Z{first_param} Trouble"
        case "01_0016":
            text = f"24Hr Medical Z{first_param} Trouble Restore"
        case "01_0017":
            text = f"24Hr Medical Z{first_param} Bypass"
        case "01_0018":
            text = f"24Hr Medical Z{first_param} UnBypass"
        case "01_0019":
            text = f"24Hr Tamper Z{first_param} Alarm"
        case "01_0020":
            text = f"24Hr Tamper Z{first_param} Alarm Restore"
        case "01_0021":
            text = f"24Hr Tamper Z{first_param} Trouble"
        case "01_0022":
            text = f"24Hr Tamper Z{first_param} Trouble Restore"
        case "01_0023":
            text = f"24Hr Tamper Z{first_param} Bypass"
        case "01_0024":
            text = f"24Hr Tamper Z{first_param} UnBypass"
        case "01_0025":
            text = f"24Hr Panic Z{first_param} Alarm"
        case "01_0026":
            text = f"24Hr Panic Z{first_param} Alarm Restore"
        case "01_0027":
            text = f"24Hr Panic Z{first_param} Trouble"
        case "01_0028":
            text = f"24Hr Panic Z{first_param} Trouble Restore"
        case "01_0029":
            text = f"24Hr Panic Z{first_param} Bypass"
        case "01_0030":
            text = f"24Hr Panic Z{first_param} UnBypass"
        case "01_0031":
            text = f"24Hr Hold-Up Z{first_param} Alarm"
        case "01_0032":
            text = f"24Hr Hold-Up Z{first_param} Alarm Restore"
        case "01_0033":
            text = f"24Hr Hold-Up Z{first_param} Trouble"
        case "01_0034":
            text = f"24Hr Hold-Up Z{first_param} Trouble Restore"
        case "01_0035":
            text = f"24Hr Hold-Up Z{first_param} Bypass"
        case "01_0036":
            text = f"24Hr Hold-Up Z{first_param} UnBypass"
        case "01_0037":
            text = f"24Hr Fire Z{first_param} Alarm"
        case "01_0038":
            text = f"24Hr Fire Z{first_param} Alarm Restore"
        case "01_0039":
            text = f"24Hr Fire Z{first_param} Trouble"
        case "01_0040":
            text = f"24Hr Fire Z{first_param} Trouble Restore"
        case "01_0041":
            text = f"24Hr Fire Z{first_param} Bypass"
        case "01_0042":
            text = f"24Hr Fire Z{first_param} UnBypass"
        case "01_0043":
            text = f"Sensor {first_param} Watch Fail"
        case "01_0044":
            text = f"Sensor {first_param} Watch Fail Restore"
        case "01_0045":
            text = f"Sensor {first_param} Tamper"
        case "01_0046":
            text = f"Sensor {first_param} Tamper Restore"
        case "01_0047_ALink":
            text = f"A-Link Area{second_param} AWAY Arm"
        case "01_0047_ALink_NoArea":
            text = f"A-Link AWAY Arm"
        case "01_0047_Installer":
            text = f"Installer Area{second_param} AWAY Arm"
        case "01_0047_Installer_NoArea":
            text = f"Installer AWAY Arm"
        case "01_0047_PowerUp":
            text = f"PowerUp Area{second_param} AWAY Arm"
        case "01_0047_PowerUp_NoArea":
            text = f"PowerUp AWAY Arm"
        case "01_0047_Quick":
            text = f"Quick Area{second_param} AWAY Arm"
        case "01_0047_Quick_NoArea":
            text = f"Quick AWAY Arm"
        case "01_0047_Schedule":
            text = f"Schedule Area{second_param} AWAY Arm"
        case "01_0047_Schedule_NoArea":
            text = f"Schedule AWAY Arm"
        case "01_0047_Telephone":
            text = f"Telephone Area{second_param} AWAY Arm"
        case "01_0047_Telephone_NoArea":
            text = f"Telephone AWAY Arm"
        case "01_0047_User":
            text = f"User{first_param} Area{second_param} AWAY Arm"
        case "01_0047_User_NoArea":
            text = f"User{first_param} AWAY Arm"
        case "01_0048_ALink":
            text = f"A-Link Area{second_param} STAY1 Arm"
        case "01_0048_ALink_NoArea":
            text = f"A-Link STAY1 Arm"
        case "01_0048_Installer":
            text = f"Installer Area{second_param} STAY1 Arm"
        case "01_0048_Installer_NoArea":
            text = f"Installer STAY1 Arm"
        case "01_0048_PowerUp":
            text = f"PowerUp Area{second_param} STAY1 Arm"
        case "01_0048_PowerUp_NoArea":
            text = f"PowerUp STAY1 Arm"
        case "01_0048_Quick":
            text = f"Quick Area{second_param} STAY1 Arm"
        case "01_0048_Quick_NoArea":
            text = f"Quick STAY1 Arm"
        case "01_0048_Schedule":
            text = f"Schedule Area{second_param} STAY1 Arm"
        case "01_0048_Schedule_NoArea":
            text = f"Schedule STAY1 Arm"
        case "01_0048_Telephone":
            text = f"Telephone Area{second_param} STAY1 Arm"
        case "01_0048_Telephone_NoArea":
            text = f"Telephone STAY1 Arm"
        case "01_0048_User":
            text = f"User{first_param} Area{second_param} STAY1 Arm"
        case "01_0048_User_NoArea":
            text = f"User{first_param} STAY1 Arm"
        case "01_0049_ALink":
            text = f"A-Link Area{second_param} STAY2 Arm"
        case "01_0049_ALink_NoArea":
            text = f"A-Link STAY2 Arm"
        case "01_0049_Installer":
            text = f"Installer Area{second_param} STAY2 Arm"
        case "01_0049_Installer_NoArea":
            text = f"Installer STAY2 Arm"
        case "01_0049_PowerUp":
            text = f"PowerUp Area{second_param} STAY2 Arm"
        case "01_0049_PowerUp_NoArea":
            text = f"PowerUp STAY2 Arm"
        case "01_0049_Quick":
            text = f"Quick Area{second_param} STAY2 Arm"
        case "01_0049_Quick_NoArea":
            text = f"Quick STAY2 Arm"
        case "01_0049_Schedule":
            text = f"Schedule Area{second_param} STAY2 Arm"
        case "01_0049_Schedule_NoArea":
            text = f"Schedule STAY2 Arm"
        case "01_0049_Telephone":
            text = f"Telephone Area{second_param} STAY2 Arm"
        case "01_0049_Telephone_NoArea":
            text = f"Telephone STAY2 Arm"
        case "01_0049_User":
            text = f"User{first_param} Area{second_param} STAY2 Arm"
        case "01_0049_User_NoArea":
            text = f"User{first_param} STAY2 Arm"
        case "01_0050_ALink":
            text = f"A-Link Area{second_param} Disarm"
        case "01_0050_ALink_NoArea":
            text = f"A-Link Disarm"
        case "01_0050_Installer":
            text = f"Installer Area{second_param} Disarm"
        case "01_0050_Installer_NoArea":
            text = f"Installer Disarm"
        case "01_0050_PowerUp":
            text = f"PowerUp Area{second_param} Disarm"
        case "01_0050_PowerUp_NoArea":
            text = f"PowerUp Disarm"
        case "01_0050_Quick":
            text = f"Quick Area{second_param} Disarm"
        case "01_0050_Quick_NoArea":
            text = f"Quick Disarm"
        case "01_0050_Schedule":
            text = f"Schedule Area{second_param} Disarm"
        case "01_0050_Schedule_NoArea":
            text = f"Schedule Disarm"
        case "01_0050_Telephone":
            text = f"Telephone Area{second_param} Disarm"
        case "01_0050_Telephone_NoArea":
            text = f"Telephone Disarm"
        case "01_0050_User":
            text = f"User{first_param} Area{second_param} Disarm"
        case "01_0050_User_NoArea":
            text = f"User{first_param} Disarm"
        case "01_0051":
            text = f"Keyswitch Zone{first_param} Area{second_param} AWAY Arm"
        case "01_0051_NoArea":
            text = f"Keyswitch Zone{first_param} AWAY Arm"
        case "01_0052":
            text = f"Keyswitch Zone{first_param} Area{second_param} STAY1 Arm"
        case "01_0052_NoArea":
            text = f"Keyswitch Zone{first_param} STAY1 Arm"
        case "01_0053":
            text = f"Keyswitch Zone{first_param} Area{second_param} Disarm"
        case "01_0053_NoArea":
            text = f"Keyswitch Zone{first_param} Disarm"
        case "01_0054_ALink":
            text = f"A-Link Area{second_param} AWAY Arm"
        case "01_0054_ALink_NoArea":
            text = f"A-Link AWAY Arm"
        case "01_0054_Installer":
            text = f"Installer Area{second_param} AWAY Arm"
        case "01_0054_Installer_NoArea":
            text = f"Installer AWAY Arm"
        case "01_0054_PowerUp":
            text = f"PowerUp Area{second_param} AWAY Arm"
        case "01_0054_PowerUp_NoArea":
            text = f"PowerUp AWAY Arm"
        case "01_0054_Quick":
            text = f"Quick Area{second_param} AWAY Arm"
        case "01_0054_Quick_NoArea":
            text = f"Quick AWAY Arm"
        case "01_0054_Schedule":
            text = f"Schedule Area{second_param} AWAY Arm"
        case "01_0054_Schedule_NoArea":
            text = f"Schedule AWAY Arm"
        case "01_0054_Telephone":
            text = f"Telephone Area{second_param} AWAY Arm"
        case "01_0054_Telephone_NoArea":
            text = f"Telephone AWAY Arm"
        case "01_0054_User":
            text = f"User{first_param} Area{second_param} AWAY Arm"
        case "01_0054_User_NoArea":
            text = f"User{first_param} AWAY Arm"
        case "01_0055_ALink":
            text = f"A-Link Area{second_param} STAY1 Arm"
        case "01_0055_ALink_NoArea":
            text = f"A-Link STAY1 Arm"
        case "01_0055_Installer":
            text = f"Installer Area{second_param} STAY1 Arm"
        case "01_0055_Installer_NoArea":
            text = f"Installer STAY1 Arm"
        case "01_0055_PowerUp":
            text = f"PowerUp Area{second_param} STAY1 Arm"
        case "01_0055_PowerUp_NoArea":
            text = f"PowerUp STAY1 Arm"
        case "01_0055_Quick":
            text = f"Quick Area{second_param} STAY1 Arm"
        case "01_0055_Quick_NoArea":
            text = f"Quick STAY1 Arm"
        case "01_0055_Schedule":
            text = f"Schedule Area{second_param} STAY1 Arm"
        case "01_0055_Schedule_NoArea":
            text = f"Schedule STAY1 Arm"
        case "01_0055_Telephone":
            text = f"Telephone Area{second_param} STAY1 Arm"
        case "01_0055_Telephone_NoArea":
            text = f"Telephone STAY1 Arm"
        case "01_0055_User":
            text = f"User{first_param} Area{second_param} STAY1 Arm"
        case "01_0055_User_NoArea":
            text = f"User{first_param} STAY1 Arm"
        case "01_0056_ALink":
            text = f"A-Link Area{second_param} Disarm"
        case "01_0056_ALink_NoArea":
            text = f"A-Link Disarm"
        case "01_0056_Installer":
            text = f"Installer Area{second_param} Disarm"
        case "01_0056_Installer_NoArea":
            text = f"Installer Disarm"
        case "01_0056_PowerUp":
            text = f"PowerUp Area{second_param} Disarm"
        case "01_0056_PowerUp_NoArea":
            text = f"PowerUp Disarm"
        case "01_0056_Quick":
            text = f"Quick Area{second_param} Disarm"
        case "01_0056_Quick_NoArea":
            text = f"Quick Disarm"
        case "01_0056_Schedule":
            text = f"Schedule Area{second_param} Disarm"
        case "01_0056_Schedule_NoArea":
            text = f"Schedule Disarm"
        case "01_0056_Telephone":
            text = f"Telephone Area{second_param} Disarm"
        case "01_0056_Telephone_NoArea":
            text = f"Telephone Disarm"
        case "01_0056_User":
            text = f"User{first_param} Area{second_param} Disarm"
        case "01_0056_User_NoArea":
            text = f"User{first_param} Disarm"
        case "01_0057_ALink":
            text = f"A-Link Area{second_param} AWAY Arm"
        case "01_0057_ALink_NoArea":
            text = f"A-Link AWAY Arm"
        case "01_0057_Installer":
            text = f"Installer Area{second_param} AWAY Arm"
        case "01_0057_Installer_NoArea":
            text = f"Installer AWAY Arm"
        case "01_0057_PowerUp":
            text = f"PowerUp Area{second_param} AWAY Arm"
        case "01_0057_PowerUp_NoArea":
            text = f"PowerUp AWAY Arm"
        case "01_0057_Quick":
            text = f"Quick Area{second_param} AWAY Arm"
        case "01_0057_Quick_NoArea":
            text = f"Quick AWAY Arm"
        case "01_0057_Schedule":
            text = f"Schedule Area{second_param} AWAY Arm"
        case "01_0057_Schedule_NoArea":
            text = f"Schedule AWAY Arm"
        case "01_0057_Telephone":
            text = f"Telephone Area{second_param} AWAY Arm"
        case "01_0057_Telephone_NoArea":
            text = f"Telephone AWAY Arm"
        case "01_0057_User":
            text = f"User{first_param} Area{second_param} AWAY Arm"
        case "01_0057_User_NoArea":
            text = f"User{first_param} AWAY Arm"
        case "01_0058_ALink":
            text = f"A-Link Area{second_param} STAY1 Arm"
        case "01_0058_ALink_NoArea":
            text = f"A-Link STAY1 Arm"
        case "01_0058_Installer":
            text = f"Installer Area{second_param} STAY1 Arm"
        case "01_0058_Installer_NoArea":
            text = f"Installer STAY1 Arm"
        case "01_0058_PowerUp":
            text = f"PowerUp Area{second_param} STAY1 Arm"
        case "01_0058_PowerUp_NoArea":
            text = f"PowerUp STAY1 Arm"
        case "01_0058_Quick":
            text = f"Quick Area{second_param} STAY1 Arm"
        case "01_0058_Quick_NoArea":
            text = f"Quick STAY1 Arm"
        case "01_0058_Schedule":
            text = f"Schedule Area{second_param} STAY1 Arm"
        case "01_0058_Schedule_NoArea":
            text = f"Schedule STAY1 Arm"
        case "01_0058_Telephone":
            text = f"Telephone Area{second_param} STAY1 Arm"
        case "01_0058_Telephone_NoArea":
            text = f"Telephone STAY1 Arm"
        case "01_0058_User":
            text = f"User{first_param} Area{second_param} STAY1 Arm"
        case "01_0058_User_NoArea":
            text = f"User{first_param} STAY1 Arm"
        case "01_0059_ALink":
            text = f"A-Link Area{second_param} STAY2 Arm"
        case "01_0059_ALink_NoArea":
            text = f"A-Link STAY2 Arm"
        case "01_0059_Installer":
            text = f"Installer Area{second_param} STAY2 Arm"
        case "01_0059_Installer_NoArea":
            text = f"Installer STAY2 Arm"
        case "01_0059_PowerUp":
            text = f"PowerUp Area{second_param} STAY2 Arm"
        case "01_0059_PowerUp_NoArea":
            text = f"PowerUp STAY2 Arm"
        case "01_0059_Quick":
            text = f"Quick Area{second_param} STAY2 Arm"
        case "01_0059_Quick_NoArea":
            text = f"Quick STAY2 Arm"
        case "01_0059_Schedule":
            text = f"Schedule Area{second_param} STAY2 Arm"
        case "01_0059_Schedule_NoArea":
            text = f"Schedule STAY2 Arm"
        case "01_0059_Telephone":
            text = f"Telephone Area{second_param} STAY2 Arm"
        case "01_0059_Telephone_NoArea":
            text = f"Telephone STAY2 Arm"
        case "01_0059_User":
            text = f"User{first_param} Area{second_param} STAY2 Arm"
        case "01_0059_User_NoArea":
            text = f"User{first_param} STAY2 Arm"
        case "01_0060_ALink":
            text = f"A-Link Area{second_param} Disarm"
        case "01_0060_ALink_NoArea":
            text = f"A-Link Disarm"
        case "01_0060_Installer":
            text = f"Installer Area{second_param} Disarm"
        case "01_0060_Installer_NoArea":
            text = f"Installer Disarm"
        case "01_0060_PowerUp":
            text = f"PowerUp Area{second_param} Disarm"
        case "01_0060_PowerUp_NoArea":
            text = f"PowerUp Disarm"
        case "01_0060_Quick":
            text = f"Quick Area{second_param} Disarm"
        case "01_0060_Quick_NoArea":
            text = f"Quick Disarm"
        case "01_0060_Schedule":
            text = f"Schedule Area{second_param} Disarm"
        case "01_0060_Schedule_NoArea":
            text = f"Schedule Disarm"
        case "01_0060_Telephone":
            text = f"Telephone Area{second_param} Disarm"
        case "01_0060_Telephone_NoArea":
            text = f"Telephone Disarm"
        case "01_0060_User":
            text = f"User{first_param} Area{second_param} Disarm"
        case "01_0060_User_NoArea":
            text = f"User{first_param} Disarm"
        case "01_0061":
            text = f"User{first_param} Duress Alarm"
        case "01_0062":
            text = f"Codepad {first_param} Locked"
        case "01_0063":
            text = f"Codepad {first_param} Panic"
        case "01_0064":
            text = f"Keyfob {first_param} Panic"
        case "01_0065":
            text = f"Codepad {first_param} Medical"
        case "01_0066":
            text = f"Codepad {first_param} Fire"
        case "01_0067":
            text = f"AC Power Fail"
        case "01_0068":
            text = f"AC Power Restore"
        case "01_0069":
            text = f"System Low Battery"
        case "01_0070":
            text = f"System Battery Restore"
        case "01_0071":
            text = f"AUX Power Fail"
        case "01_0072":
            text = f"AUX Power Restore"
        case "01_0073":
            text = f"Panel Tamper"
        case "01_0074":
            text = f"Panel Tamper Restore"
        case "01_0075":
            text = f"RF Sensor {first_param} Low Battery"
        case "01_0076":
            text = f"RF Sensor {first_param} Battery Restore"
        case "01_0077":
            text = f"Keyfob {first_param} Low Battery"
        case "01_0078":
            text = f"Keyfob {first_param} Battery Restore"
        case "01_0079":
            text = f"RF Sensor {first_param} Missing"
        case "01_0080":
            text = f"RF Sensor {first_param} Missing Restore"
        case "01_0081":
            text = f"RF Fire Sensor {first_param} Missing"
        case "01_0082":
            text = f"RF Fire Sensor {first_param} Missing Restore"
        case "01_0083":
            text = f"RF Receiver Missing"
        case "01_0084":
            text = f"RF Receiver Missing Restore"
        case "01_0085":
            text = f"RF Receiver Jamming"
        case "01_0086":
            text = f"RF Receiver Jamming Restore"
        case "01_0087":
            text = f"RF Receiver Tamper"
        case "01_0088":
            text = f"RF Receiver Tamper Restore"
        case "01_0089":
            text = f"RF Repeater {first_param} Missing"
        case "01_0090":
            text = f"RF Repeater {first_param} Missing Restore"
        case "01_0091":
            text = f"RF Repeater Jamming"
        case "01_0092":
            text = f"RF Repeater Jamming Restore"
        case "01_0093":
            text = f"RF Repeater {first_param} Tamper"
        case "01_0094":
            text = f"RF Repeater {first_param} Tamper Restore"
        case "01_0095":
            text = f"Codepad {first_param} Missing"
        case "01_0096":
            text = f"Codepad {first_param} Missing Restore"
        case "01_0097":
            text = f"Codepad {first_param} Tamper"
        case "01_0098":
            text = f"Codepad {first_param} Tamper Restore"
        case "01_0099":
            text = f"IP Module {first_param} Missing"
        case "01_0100":
            text = f"IP Module {first_param} Missing Restore"
        case "01_0101":
            text = f"IP Module {first_param} Tamper"
        case "01_0102":
            text = f"IP Module {first_param} Tamper Restore"
        case "01_0103":
            text = f"Ex. Output {first_param} Missing"
        case "01_0104":
            text = f"Ex. Output {first_param} Missing Restore"
        case "01_0105":
            text = f"Ex. Output {first_param} Tamper"
        case "01_0106":
            text = f"Ex. Output {first_param} Tamper Restore"
        case "01_0107":
            text = f"Walk Test Begin"
        case "01_0108":
            text = f"Walk Test End"
        case "01_0109":
            text = f"Program Change"
        case "01_0110_ALink":
            text = f"A-Link Set Clock"
        case "01_0110_User":
            text = f"User{first_param} Set Clock"
        case "01_0111":
            text = f"Phone Line Fail"
        case "01_0112":
            text = f"Phone Line Restore"
        case "01_0113":
            text = f"Warning Device Fail"
        case "01_0114":
            text = f"Warning Device Restore"
        case "01_0115":
            text = f"Comm Fail"
        case "01_0116":
            text = f"Comm Restore"
        case "01_0117":
            text = f"Comm Manual Test"
        case "01_0118":
            text = f"Comm Auto Test"
        case "01_0119":
            text = f"ExInput {first_param} Missing"
        case "01_0120":
            text = f"ExInput {first_param} Missing Restore"
        case "01_0121":
            text = f"ExInput {first_param} Tamper"
        case "01_0122":
            text = f"ExInput {first_param} Tamper Restore"
        case "01_0123":
            text = f"PUSH FAIL MOD {first_param}"
        case "01_0124":
            text = f"PUSH RES. MOD {first_param}"
        case "99_0000":
            text = f"System reset"
        case "99_0001":
            text = f"Away Arm: area {first_param}"
        case "99_0002":
            text = f"System disarm"
        case "99_0003":
            text = f"Panic alarm: area {first_param} zone {second_param}"
    return text