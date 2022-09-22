def solutions_key(first_param):
        if first_param >= 1 and first_param <= 32:
            return "_User"
        
        param = [[0, "_Quick"],
                [994, "PowerUp"],
                [995, "_Telephone"],
                [997, "_Schedule"],
                [998, "_ALink"],
                [999, "_Installer"]]
        for p in param:
            for i in param[p]:
                if first_param == param[p][0]:
                    return param[p][1]
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
    if first_param == 0:
        return "_Installer"
    if first_param == 251:
        return "_RPC"
    if first_param == 252:
        return "_Remote"
    if first_param == 253:
        return "_QuickArm"
    if first_param == 254:
        return "_KeySwitch"
    return "_User"
def parse_history_message(eventCode, first_param, second_param, panel_type_name):
    event_type = "99"
    if "AMAX" in panel_type_name:
        event_type = "00"
    if "Solution" in panel_type_name:
        event_type = "01"
    key = f"{event_type}_{str(eventCode).rjust(4,'0')}"
    if event_type == "00":
        if eventCode == 26:
            if first_param == 0:
                key += "_Auto"
            else:
                key += "_Manual"
        if eventCode in (62, 63, 105, 106, 107, 108, 109):
            if first_param == 134:
                key += "_MODULE1"
            elif first_param == 250:
                key += "_MODULE2"
        if eventCode == 30 or eventCode == 31:
            key += amax_module_key(first_param)
        if eventCode == 32 or eventCode == 33:
            key += amax_tamper_key(first_param)
    if event_type == "01":
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
    if key == "00_0000":
        return f"System reset"
    if key == "00_0001":
        return f"Area {second_param}, zone {first_param} burglary alarm"
    if key == "00_0002":
        return f"Area {second_param}, zone {first_param} burglary alarm restore"
    if key == "00_0003":
        return f"Area {second_param}, zone {first_param} 24 hour burglary alarm"
    if key == "00_0004":
        return f"Area {second_param}, zone {first_param} 24 hour burglary alarm restore"
    if key == "00_0005":
        return f"Area {second_param}, zone {first_param} burglary trouble"
    if key == "00_0006":
        return f"Area {second_param}, zone {first_param} burglary trouble restore"
    if key == "00_0007":
        return f"Area {second_param}, zone {first_param} burglary bypass"
    if key == "00_0008":
        return f"Area {second_param}, zone {first_param} burglary bypass restore"
    if key == "00_0009":
        return f"Area {second_param}, zone {first_param} Tamper alarm"
    if key == "00_0010":
        return f"Area {second_param}, zone {first_param} Tamper restore"
    if key == "00_0011_Installer":
        return f"Area {first_param} arm by installer (AWAY)"
    if key == "00_0011_KeySwitch":
        return f"Area {first_param} arm by key switch (AWAY)"
    if key == "00_0011_QuickArm":
        return f"Area {first_param} arm by quick arm (AWAY)"
    if key == "00_0011_RPC":
        return f"Area {first_param} arm by RPC (AWAY)"
    if key == "00_0011_Remote":
        return f"Area {first_param} arm by remote(AWAY)"
    if key == "00_0011_User":
        return f"Area {second_param} arm by user {first_param} (AWAY)"
    if key == "00_0012_Installer":
        return f"Area {first_param} disarm by installer(AWAY)"
    if key == "00_0012_KeySwitch":
        return f"Area {first_param} disarm by key switch (AWAY)"
    if key == "00_0012_RPC":
        return f"Area {first_param} disarm by RPC (AWAY)"
    if key == "00_0012_User":
        return f"Area {second_param} disarm by user {first_param} (AWAY)"
    if key == "00_0013_Installer":
        return f"Area {first_param} arm by installer (STAY)"
    if key == "00_0013_KeySwitch":
        return f"Area {first_param} arm by key switch (STAY)"
    if key == "00_0013_QuickArm":
        return f"Area {first_param} arm by quick arm (STAY)"
    if key == "00_0013_RPC":
        return f"Area {first_param} arm by RPC (STAY)"
    if key == "00_0013_User":
        return f"Area {second_param} arm by user {first_param} (STAY)"
    if key == "00_0014_Installer":
        return f"Area {first_param} disarm by installer(STAY)"
    if key == "00_0014_KeySwitch":
        return f"Area {first_param} disarm by key switch (STAY)"
    if key == "00_0014_RPC":
        return f"Area {first_param} disarm by RPC (STAY)"
    if key == "00_0014_User":
        return f"Area {second_param} disarm by user {first_param} (STAY)"
    if key == "00_0015":
        return f"Keypad emergency"
    if key == "00_0016":
        return f"Keypad fire"
    if key == "00_0017":
        return f"Keypad medical"
    if key == "00_0018":
        return f"Duress by user {first_param}"
    if key == "00_0019":
        return f"Keypad no.# {first_param} lockout"
    if key == "00_0020":
        return f"Low battery"
    if key == "00_0021":
        return f"Battery restore"
    if key == "00_0022":
        return f"AC fail"
    if key == "00_0023":
        return f"AC restore"
    if key == "00_0024":
        return f"AUX power fail {first_param}"
    if key == "00_0025":
        return f"AUX power restore {first_param}"
    if key == "00_0026_Auto":
        return f"Communication test"
    if key == "00_0026_Manual":
        return f"Communication test"
    if key == "00_0027":
        return f"Configuration change"
    if key == "00_0028":
        return f"Communications destination {first_param} trouble"
    if key == "00_0029":
        return f"Communications destination {first_param} trouble restore"
    if key == "00_0030_InputModule":
        return f"DX2010-CHI trouble {first_param}"
    if key == "00_0030_IpModule":
        return f"B420-CN/DX4020-G trouble {first_param}"
    if key == "00_0030_Keypad":
        return f"Keypad trouble {first_param}"
    if key == "00_0030_RelayOutputModule":
        return f"DX3010 trouble {first_param}"
    if key == "00_0031_InputModule":
        return f"DX2010-CHI trouble restore {first_param}"
    if key == "00_0031_IpModule":
        return f"B420-CN/DX4020-G trouble restore {first_param}"
    if key == "00_0031_Keypad":
        return f"Keypad trouble restore {first_param}"
    if key == "00_0031_RelayOutputModule":
        return f"DX3010 trouble restore {first_param}"
    if key == "00_0032_InputModule":
        return f"DX2010-CHI tamper {first_param}"
    if key == "00_0032_Keypad":
        return f"Keypad tamper"
    if key == "00_0032_OnboardTamper":
        return f"Onboard tamper"
    if key == "00_0033_InputModule":
        return f"DX2010-CHI tamper restore {first_param}"
    if key == "00_0033_Keypad":
        return f"Keypad tamper restore"
    if key == "00_0033_OnboardTamper":
        return f"Onboard tamper restore"
    if key == "00_0034":
        return f"Date/time setting"
    if key == "00_0035":
        return f"User code {first_param} change"
    if key == "00_0036":
        return f"Enter program mode"
    if key == "00_0037":
        return f"Exit program mode"
    if key == "00_0038":
        return f"Phone line fail"
    if key == "00_0039":
        return f"Phone line restore"
    if key == "00_0040":
        return f"Area {second_param}, zone {first_param} 24 hour panic alarm"
    if key == "00_0041":
        return f"Area {second_param}, zone {first_param} 24 hour panic alarm restore"
    if key == "00_0042":
        return f"Area {second_param}, zone {first_param} 24 hour fire"
    if key == "00_0043":
        return f"Area {second_param}, zone {first_param} 24 hour fire restore"
    if key == "00_0044":
        return f"Area {second_param}, zone {first_param} fire unverified"
    if key == "00_0045":
        return f"{first_param} Output fault"
    if key == "00_0046":
        return f"{first_param} Output fault restore"
    if key == "00_0047":
        return f"Summer time"
    if key == "00_0048":
        return f"Winter time"
    if key == "00_0049":
        return f"Fault override"
    if key == "00_0050":
        return f"Panel access"
    if key == "00_0051":
        return f"Software update"
    if key == "00_0052":
        return f"Remote link success"
    if key == "00_0053":
        return f"Clock fail"
    if key == "00_0054":
        return f"Area {second_param}, zone {first_param} tamper alarm"
    if key == "00_0055":
        return f"Area {second_param}, zone {first_param} tamper restore"
    if key == "00_0056":
        return f"Area {second_param}, zone {first_param} zone EXT fault"
    if key == "00_0057":
        return f"Area {second_param}, zone {first_param} zone EXT fault restore"
    if key == "00_0058":
        return f"Area {second_param}, zone {first_param} exit delay"
    if key == "00_0059":
        return f"Area {second_param}, zone {first_param} exit delay restore"
    if key == "00_0060":
        return f"Area {second_param}, zone {first_param} burglary alarm verified"
    if key == "00_0061":
        return f"Area {second_param}, zone {first_param} burglary alarm unverified"
    if key == "00_0062_MODULE1":
        return f"IP module trouble #1"
    if key == "00_0062_MODULE2":
        return f"IP module trouble #2"
    if key == "00_0063_MODULE1":
        return f"IP module restore #1"
    if key == "00_0063_MODULE2":
        return f"IP module restore #2"
    if key == "00_0064":
        return f"Printer missing"
    if key == "00_0065":
        return f"Printer missing restore"
    if key == "00_0066":
        return f"Printer error"
    if key == "00_0067":
        return f"Printer error restore"
    if key == "00_0068":
        return f"Expansion device missing"
    if key == "00_0069":
        return f"Expansion device missing restore"
    if key == "00_0070":
        return f"Expansion missing"
    if key == "00_0071":
        return f"Expansion missing restore"
    if key == "00_0072":
        return f"Expansion device tamper"
    if key == "00_0073":
        return f"Expansion tamper restore"
    if key == "00_0074":
        return f"Expansion trouble"
    if key == "00_0075":
        return f"Expansion trouble restore"
    if key == "00_0076":
        return f"Wireless receiver jam"
    if key == "00_0077":
        return f"Wireless receiver jam restore"
    if key == "00_0078_RfRepeater":
        return f"Area {second_param} wireless zone {first_param} receiver config conflict"
    if key == "00_0078_RfZone":
        return f"Area {second_param} wireless zone {first_param} receiver config conflict"
    if key == "00_0078_User":
        return f"Area {second_param} wireless zone {first_param} receiver config conflict"
    if key == "00_0079_RfRepeater":
        return f"Area {second_param} wireless zone {first_param} receiver config conflict restore"
    if key == "00_0079_RfZone":
        return f"Area {second_param} wireless zone {first_param} receiver config conflict restore"
    if key == "00_0079_User":
        return f"Area {second_param} wireless zone {first_param} receiver config conflict restore"
    if key == "00_0080":
        return f"Area {second_param} wireless zone {first_param} missing"
    if key == "00_0081":
        return f"Area {second_param} wireless zone {first_param} missing restore"
    if key == "00_0082":
        return f"Area {second_param} wireless zone {first_param} low battery"
    if key == "00_0083":
        return f"Area {second_param} wireless zone {first_param} low battery restore"
    if key == "00_0084":
        return f"Area {second_param} wireless zone {first_param} trouble"
    if key == "00_0085":
        return f"Area {second_param} wireless zone {first_param} trouble restore"
    if key == "00_0086":
        return f"Wireless repeater {first_param} missing"
    if key == "00_0087":
        return f"Wireless repeater {first_param} missing restore"
    if key == "00_0088":
        return f"Wireless repeater {first_param} low battery"
    if key == "00_0089":
        return f"Wireless repeater {first_param} low battery restore"
    if key == "00_0090":
        return f"Wireless repeater {first_param} tamper"
    if key == "00_0091":
        return f"Wireless repeater {first_param} tamper restore"
    if key == "00_0092":
        return f"Wireless repeater {first_param} AC fail"
    if key == "00_0093":
        return f"Wireless repeater {first_param} AC fail restore"
    if key == "00_0094":
        return f"Wireless keyfob {first_param} low battery"
    if key == "00_0095":
        return f"Wireless keyfob {first_param} low battery restore"
    if key == "00_0096":
        return f"Wireless keyfob {first_param} panic alarm"
    if key == "00_0097":
        return f"Wireless keyfob {first_param} silent alarm"
    if key == "00_0098":
        return f"Wireless change keyfob {first_param}"
    if key == "00_0099":
        return f"Area {second_param} wireless zone {first_param} enclosure tamper"
    if key == "00_0100":
        return f"Area {second_param} wireless zone {first_param} enclosure tamper restore"
    if key == "00_0101":
        return f"Area {second_param} wireless zone {first_param} missing"
    if key == "00_0102":
        return f"Area {second_param} wireless zone {first_param} restore"
    if key == "00_0103":
        return f"Service mode on"
    if key == "00_0104":
        return f"Service mode off"
    if key == "00_0105_MODULE1":
        return f"Network config changed #1"
    if key == "00_0105_MODULE2":
        return f"Network config changed #2"
    if key == "00_0106_MODULE1":
        return f"Network trouble #1"
    if key == "00_0106_MODULE2":
        return f"Network trouble #2"
    if key == "00_0107_MODULE1":
        return f"Network restore #1"
    if key == "00_0107_MODULE2":
        return f"Network restore #2"
    if key == "00_0108_MODULE1":
        return f"Push fail #1"
    if key == "00_0108_MODULE2":
        return f"Push fail #2"
    if key == "00_0109_MODULE1":
        return f"Push restore #1"
    if key == "00_0109_MODULE2":
        return f"Push restore #2"
    if key == "01_0000":
        return f"System reset"
    if key == "01_0001":
        return f"Z{first_param} Alarm"
    if key == "01_0002":
        return f"Z{first_param} Alarm Restore"
    if key == "01_0003":
        return f"Z{first_param} Trouble"
    if key == "01_0004":
        return f"Z{first_param} Trouble Restore"
    if key == "01_0005":
        return f"Z{first_param} Bypass"
    if key == "01_0006":
        return f"Z{first_param} UnBypass"
    if key == "01_0007":
        return f"24Hr Z{first_param} Alarm"
    if key == "01_0008":
        return f"24Hr Z{first_param} Alarm Restore"
    if key == "01_0009":
        return f"24Hr Z{first_param} Trouble"
    if key == "01_0010":
        return f"24Hr Z{first_param} Trouble Restore"
    if key == "01_0011":
        return f"24Hr Z{first_param} Bypass"
    if key == "01_0012":
        return f"24Hr Z{first_param} UnBypass"
    if key == "01_0013":
        return f"24Hr Medical Z{first_param} Alarm"
    if key == "01_0014":
        return f"24Hr Medical Z{first_param} Alarm Restore"
    if key == "01_0015":
        return f"24Hr Medical Z{first_param} Trouble"
    if key == "01_0016":
        return f"24Hr Medical Z{first_param} Trouble Restore"
    if key == "01_0017":
        return f"24Hr Medical Z{first_param} Bypass"
    if key == "01_0018":
        return f"24Hr Medical Z{first_param} UnBypass"
    if key == "01_0019":
        return f"24Hr Tamper Z{first_param} Alarm"
    if key == "01_0020":
        return f"24Hr Tamper Z{first_param} Alarm Restore"
    if key == "01_0021":
        return f"24Hr Tamper Z{first_param} Trouble"
    if key == "01_0022":
        return f"24Hr Tamper Z{first_param} Trouble Restore"
    if key == "01_0023":
        return f"24Hr Tamper Z{first_param} Bypass"
    if key == "01_0024":
        return f"24Hr Tamper Z{first_param} UnBypass"
    if key == "01_0025":
        return f"24Hr Panic Z{first_param} Alarm"
    if key == "01_0026":
        return f"24Hr Panic Z{first_param} Alarm Restore"
    if key == "01_0027":
        return f"24Hr Panic Z{first_param} Trouble"
    if key == "01_0028":
        return f"24Hr Panic Z{first_param} Trouble Restore"
    if key == "01_0029":
        return f"24Hr Panic Z{first_param} Bypass"
    if key == "01_0030":
        return f"24Hr Panic Z{first_param} UnBypass"
    if key == "01_0031":
        return f"24Hr Hold-Up Z{first_param} Alarm"
    if key == "01_0032":
        return f"24Hr Hold-Up Z{first_param} Alarm Restore"
    if key == "01_0033":
        return f"24Hr Hold-Up Z{first_param} Trouble"
    if key == "01_0034":
        return f"24Hr Hold-Up Z{first_param} Trouble Restore"
    if key == "01_0035":
        return f"24Hr Hold-Up Z{first_param} Bypass"
    if key == "01_0036":
        return f"24Hr Hold-Up Z{first_param} UnBypass"
    if key == "01_0037":
        return f"24Hr Fire Z{first_param} Alarm"
    if key == "01_0038":
        return f"24Hr Fire Z{first_param} Alarm Restore"
    if key == "01_0039":
        return f"24Hr Fire Z{first_param} Trouble"
    if key == "01_0040":
        return f"24Hr Fire Z{first_param} Trouble Restore"
    if key == "01_0041":
        return f"24Hr Fire Z{first_param} Bypass"
    if key == "01_0042":
        return f"24Hr Fire Z{first_param} UnBypass"
    if key == "01_0043":
        return f"Sensor {first_param} Watch Fail"
    if key == "01_0044":
        return f"Sensor {first_param} Watch Fail Restore"
    if key == "01_0045":
        return f"Sensor {first_param} Tamper"
    if key == "01_0046":
        return f"Sensor {first_param} Tamper Restore"
    if key == "01_0047_ALink":
        return f"A-Link Area{second_param} AWAY Arm"
    if key == "01_0047_ALink_NoArea":
        return f"A-Link AWAY Arm"
    if key == "01_0047_Installer":
        return f"Installer Area{second_param} AWAY Arm"
    if key == "01_0047_Installer_NoArea":
        return f"Installer AWAY Arm"
    if key == "01_0047_PowerUp":
        return f"PowerUp Area{second_param} AWAY Arm"
    if key == "01_0047_PowerUp_NoArea":
        return f"PowerUp AWAY Arm"
    if key == "01_0047_Quick":
        return f"Quick Area{second_param} AWAY Arm"
    if key == "01_0047_Quick_NoArea":
        return f"Quick AWAY Arm"
    if key == "01_0047_Schedule":
        return f"Schedule Area{second_param} AWAY Arm"
    if key == "01_0047_Schedule_NoArea":
        return f"Schedule AWAY Arm"
    if key == "01_0047_Telephone":
        return f"Telephone Area{second_param} AWAY Arm"
    if key == "01_0047_Telephone_NoArea":
        return f"Telephone AWAY Arm"
    if key == "01_0047_User":
        return f"User{first_param} Area{second_param} AWAY Arm"
    if key == "01_0047_User_NoArea":
        return f"User{first_param} AWAY Arm"
    if key == "01_0048_ALink":
        return f"A-Link Area{second_param} STAY1 Arm"
    if key == "01_0048_ALink_NoArea":
        return f"A-Link STAY1 Arm"
    if key == "01_0048_Installer":
        return f"Installer Area{second_param} STAY1 Arm"
    if key == "01_0048_Installer_NoArea":
        return f"Installer STAY1 Arm"
    if key == "01_0048_PowerUp":
        return f"PowerUp Area{second_param} STAY1 Arm"
    if key == "01_0048_PowerUp_NoArea":
        return f"PowerUp STAY1 Arm"
    if key == "01_0048_Quick":
        return f"Quick Area{second_param} STAY1 Arm"
    if key == "01_0048_Quick_NoArea":
        return f"Quick STAY1 Arm"
    if key == "01_0048_Schedule":
        return f"Schedule Area{second_param} STAY1 Arm"
    if key == "01_0048_Schedule_NoArea":
        return f"Schedule STAY1 Arm"
    if key == "01_0048_Telephone":
        return f"Telephone Area{second_param} STAY1 Arm"
    if key == "01_0048_Telephone_NoArea":
        return f"Telephone STAY1 Arm"
    if key == "01_0048_User":
        return f"User{first_param} Area{second_param} STAY1 Arm"
    if key == "01_0048_User_NoArea":
        return f"User{first_param} STAY1 Arm"
    if key == "01_0049_ALink":
        return f"A-Link Area{second_param} STAY2 Arm"
    if key == "01_0049_ALink_NoArea":
        return f"A-Link STAY2 Arm"
    if key == "01_0049_Installer":
        return f"Installer Area{second_param} STAY2 Arm"
    if key == "01_0049_Installer_NoArea":
        return f"Installer STAY2 Arm"
    if key == "01_0049_PowerUp":
        return f"PowerUp Area{second_param} STAY2 Arm"
    if key == "01_0049_PowerUp_NoArea":
        return f"PowerUp STAY2 Arm"
    if key == "01_0049_Quick":
        return f"Quick Area{second_param} STAY2 Arm"
    if key == "01_0049_Quick_NoArea":
        return f"Quick STAY2 Arm"
    if key == "01_0049_Schedule":
        return f"Schedule Area{second_param} STAY2 Arm"
    if key == "01_0049_Schedule_NoArea":
        return f"Schedule STAY2 Arm"
    if key == "01_0049_Telephone":
        return f"Telephone Area{second_param} STAY2 Arm"
    if key == "01_0049_Telephone_NoArea":
        return f"Telephone STAY2 Arm"
    if key == "01_0049_User":
        return f"User{first_param} Area{second_param} STAY2 Arm"
    if key == "01_0049_User_NoArea":
        return f"User{first_param} STAY2 Arm"
    if key == "01_0050_ALink":
        return f"A-Link Area{second_param} Disarm"
    if key == "01_0050_ALink_NoArea":
        return f"A-Link Disarm"
    if key == "01_0050_Installer":
        return f"Installer Area{second_param} Disarm"
    if key == "01_0050_Installer_NoArea":
        return f"Installer Disarm"
    if key == "01_0050_PowerUp":
        return f"PowerUp Area{second_param} Disarm"
    if key == "01_0050_PowerUp_NoArea":
        return f"PowerUp Disarm"
    if key == "01_0050_Quick":
        return f"Quick Area{second_param} Disarm"
    if key == "01_0050_Quick_NoArea":
        return f"Quick Disarm"
    if key == "01_0050_Schedule":
        return f"Schedule Area{second_param} Disarm"
    if key == "01_0050_Schedule_NoArea":
        return f"Schedule Disarm"
    if key == "01_0050_Telephone":
        return f"Telephone Area{second_param} Disarm"
    if key == "01_0050_Telephone_NoArea":
        return f"Telephone Disarm"
    if key == "01_0050_User":
        return f"User{first_param} Area{second_param} Disarm"
    if key == "01_0050_User_NoArea":
        return f"User{first_param} Disarm"
    if key == "01_0051":
        return f"Keyswitch Zone{first_param} Area{second_param} AWAY Arm"
    if key == "01_0051_NoArea":
        return f"Keyswitch Zone{first_param} AWAY Arm"
    if key == "01_0052":
        return f"Keyswitch Zone{first_param} Area{second_param} STAY1 Arm"
    if key == "01_0052_NoArea":
        return f"Keyswitch Zone{first_param} STAY1 Arm"
    if key == "01_0053":
        return f"Keyswitch Zone{first_param} Area{second_param} Disarm"
    if key == "01_0053_NoArea":
        return f"Keyswitch Zone{first_param} Disarm"
    if key == "01_0054_ALink":
        return f"A-Link Area{second_param} AWAY Arm"
    if key == "01_0054_ALink_NoArea":
        return f"A-Link AWAY Arm"
    if key == "01_0054_Installer":
        return f"Installer Area{second_param} AWAY Arm"
    if key == "01_0054_Installer_NoArea":
        return f"Installer AWAY Arm"
    if key == "01_0054_PowerUp":
        return f"PowerUp Area{second_param} AWAY Arm"
    if key == "01_0054_PowerUp_NoArea":
        return f"PowerUp AWAY Arm"
    if key == "01_0054_Quick":
        return f"Quick Area{second_param} AWAY Arm"
    if key == "01_0054_Quick_NoArea":
        return f"Quick AWAY Arm"
    if key == "01_0054_Schedule":
        return f"Schedule Area{second_param} AWAY Arm"
    if key == "01_0054_Schedule_NoArea":
        return f"Schedule AWAY Arm"
    if key == "01_0054_Telephone":
        return f"Telephone Area{second_param} AWAY Arm"
    if key == "01_0054_Telephone_NoArea":
        return f"Telephone AWAY Arm"
    if key == "01_0054_User":
        return f"User{first_param} Area{second_param} AWAY Arm"
    if key == "01_0054_User_NoArea":
        return f"User{first_param} AWAY Arm"
    if key == "01_0055_ALink":
        return f"A-Link Area{second_param} STAY1 Arm"
    if key == "01_0055_ALink_NoArea":
        return f"A-Link STAY1 Arm"
    if key == "01_0055_Installer":
        return f"Installer Area{second_param} STAY1 Arm"
    if key == "01_0055_Installer_NoArea":
        return f"Installer STAY1 Arm"
    if key == "01_0055_PowerUp":
        return f"PowerUp Area{second_param} STAY1 Arm"
    if key == "01_0055_PowerUp_NoArea":
        return f"PowerUp STAY1 Arm"
    if key == "01_0055_Quick":
        return f"Quick Area{second_param} STAY1 Arm"
    if key == "01_0055_Quick_NoArea":
        return f"Quick STAY1 Arm"
    if key == "01_0055_Schedule":
        return f"Schedule Area{second_param} STAY1 Arm"
    if key == "01_0055_Schedule_NoArea":
        return f"Schedule STAY1 Arm"
    if key == "01_0055_Telephone":
        return f"Telephone Area{second_param} STAY1 Arm"
    if key == "01_0055_Telephone_NoArea":
        return f"Telephone STAY1 Arm"
    if key == "01_0055_User":
        return f"User{first_param} Area{second_param} STAY1 Arm"
    if key == "01_0055_User_NoArea":
        return f"User{first_param} STAY1 Arm"
    if key == "01_0056_ALink":
        return f"A-Link Area{second_param} Disarm"
    if key == "01_0056_ALink_NoArea":
        return f"A-Link Disarm"
    if key == "01_0056_Installer":
        return f"Installer Area{second_param} Disarm"
    if key == "01_0056_Installer_NoArea":
        return f"Installer Disarm"
    if key == "01_0056_PowerUp":
        return f"PowerUp Area{second_param} Disarm"
    if key == "01_0056_PowerUp_NoArea":
        return f"PowerUp Disarm"
    if key == "01_0056_Quick":
        return f"Quick Area{second_param} Disarm"
    if key == "01_0056_Quick_NoArea":
        return f"Quick Disarm"
    if key == "01_0056_Schedule":
        return f"Schedule Area{second_param} Disarm"
    if key == "01_0056_Schedule_NoArea":
        return f"Schedule Disarm"
    if key == "01_0056_Telephone":
        return f"Telephone Area{second_param} Disarm"
    if key == "01_0056_Telephone_NoArea":
        return f"Telephone Disarm"
    if key == "01_0056_User":
        return f"User{first_param} Area{second_param} Disarm"
    if key == "01_0056_User_NoArea":
        return f"User{first_param} Disarm"
    if key == "01_0057_ALink":
        return f"A-Link Area{second_param} AWAY Arm"
    if key == "01_0057_ALink_NoArea":
        return f"A-Link AWAY Arm"
    if key == "01_0057_Installer":
        return f"Installer Area{second_param} AWAY Arm"
    if key == "01_0057_Installer_NoArea":
        return f"Installer AWAY Arm"
    if key == "01_0057_PowerUp":
        return f"PowerUp Area{second_param} AWAY Arm"
    if key == "01_0057_PowerUp_NoArea":
        return f"PowerUp AWAY Arm"
    if key == "01_0057_Quick":
        return f"Quick Area{second_param} AWAY Arm"
    if key == "01_0057_Quick_NoArea":
        return f"Quick AWAY Arm"
    if key == "01_0057_Schedule":
        return f"Schedule Area{second_param} AWAY Arm"
    if key == "01_0057_Schedule_NoArea":
        return f"Schedule AWAY Arm"
    if key == "01_0057_Telephone":
        return f"Telephone Area{second_param} AWAY Arm"
    if key == "01_0057_Telephone_NoArea":
        return f"Telephone AWAY Arm"
    if key == "01_0057_User":
        return f"User{first_param} Area{second_param} AWAY Arm"
    if key == "01_0057_User_NoArea":
        return f"User{first_param} AWAY Arm"
    if key == "01_0058_ALink":
        return f"A-Link Area{second_param} STAY1 Arm"
    if key == "01_0058_ALink_NoArea":
        return f"A-Link STAY1 Arm"
    if key == "01_0058_Installer":
        return f"Installer Area{second_param} STAY1 Arm"
    if key == "01_0058_Installer_NoArea":
        return f"Installer STAY1 Arm"
    if key == "01_0058_PowerUp":
        return f"PowerUp Area{second_param} STAY1 Arm"
    if key == "01_0058_PowerUp_NoArea":
        return f"PowerUp STAY1 Arm"
    if key == "01_0058_Quick":
        return f"Quick Area{second_param} STAY1 Arm"
    if key == "01_0058_Quick_NoArea":
        return f"Quick STAY1 Arm"
    if key == "01_0058_Schedule":
        return f"Schedule Area{second_param} STAY1 Arm"
    if key == "01_0058_Schedule_NoArea":
        return f"Schedule STAY1 Arm"
    if key == "01_0058_Telephone":
        return f"Telephone Area{second_param} STAY1 Arm"
    if key == "01_0058_Telephone_NoArea":
        return f"Telephone STAY1 Arm"
    if key == "01_0058_User":
        return f"User{first_param} Area{second_param} STAY1 Arm"
    if key == "01_0058_User_NoArea":
        return f"User{first_param} STAY1 Arm"
    if key == "01_0059_ALink":
        return f"A-Link Area{second_param} STAY2 Arm"
    if key == "01_0059_ALink_NoArea":
        return f"A-Link STAY2 Arm"
    if key == "01_0059_Installer":
        return f"Installer Area{second_param} STAY2 Arm"
    if key == "01_0059_Installer_NoArea":
        return f"Installer STAY2 Arm"
    if key == "01_0059_PowerUp":
        return f"PowerUp Area{second_param} STAY2 Arm"
    if key == "01_0059_PowerUp_NoArea":
        return f"PowerUp STAY2 Arm"
    if key == "01_0059_Quick":
        return f"Quick Area{second_param} STAY2 Arm"
    if key == "01_0059_Quick_NoArea":
        return f"Quick STAY2 Arm"
    if key == "01_0059_Schedule":
        return f"Schedule Area{second_param} STAY2 Arm"
    if key == "01_0059_Schedule_NoArea":
        return f"Schedule STAY2 Arm"
    if key == "01_0059_Telephone":
        return f"Telephone Area{second_param} STAY2 Arm"
    if key == "01_0059_Telephone_NoArea":
        return f"Telephone STAY2 Arm"
    if key == "01_0059_User":
        return f"User{first_param} Area{second_param} STAY2 Arm"
    if key == "01_0059_User_NoArea":
        return f"User{first_param} STAY2 Arm"
    if key == "01_0060_ALink":
        return f"A-Link Area{second_param} Disarm"
    if key == "01_0060_ALink_NoArea":
        return f"A-Link Disarm"
    if key == "01_0060_Installer":
        return f"Installer Area{second_param} Disarm"
    if key == "01_0060_Installer_NoArea":
        return f"Installer Disarm"
    if key == "01_0060_PowerUp":
        return f"PowerUp Area{second_param} Disarm"
    if key == "01_0060_PowerUp_NoArea":
        return f"PowerUp Disarm"
    if key == "01_0060_Quick":
        return f"Quick Area{second_param} Disarm"
    if key == "01_0060_Quick_NoArea":
        return f"Quick Disarm"
    if key == "01_0060_Schedule":
        return f"Schedule Area{second_param} Disarm"
    if key == "01_0060_Schedule_NoArea":
        return f"Schedule Disarm"
    if key == "01_0060_Telephone":
        return f"Telephone Area{second_param} Disarm"
    if key == "01_0060_Telephone_NoArea":
        return f"Telephone Disarm"
    if key == "01_0060_User":
        return f"User{first_param} Area{second_param} Disarm"
    if key == "01_0060_User_NoArea":
        return f"User{first_param} Disarm"
    if key == "01_0061":
        return f"User{first_param} Duress Alarm"
    if key == "01_0062":
        return f"Codepad {first_param} Locked"
    if key == "01_0063":
        return f"Codepad {first_param} Panic"
    if key == "01_0064":
        return f"Keyfob {first_param} Panic"
    if key == "01_0065":
        return f"Codepad {first_param} Medical"
    if key == "01_0066":
        return f"Codepad {first_param} Fire"
    if key == "01_0067":
        return f"AC Power Fail"
    if key == "01_0068":
        return f"AC Power Restore"
    if key == "01_0069":
        return f"System Low Battery"
    if key == "01_0070":
        return f"System Battery Restore"
    if key == "01_0071":
        return f"AUX Power Fail"
    if key == "01_0072":
        return f"AUX Power Restore"
    if key == "01_0073":
        return f"Panel Tamper"
    if key == "01_0074":
        return f"Panel Tamper Restore"
    if key == "01_0075":
        return f"RF Sensor {first_param} Low Battery"
    if key == "01_0076":
        return f"RF Sensor {first_param} Battery Restore"
    if key == "01_0077":
        return f"Keyfob {first_param} Low Battery"
    if key == "01_0078":
        return f"Keyfob {first_param} Battery Restore"
    if key == "01_0079":
        return f"RF Sensor {first_param} Missing"
    if key == "01_0080":
        return f"RF Sensor {first_param} Missing Restore"
    if key == "01_0081":
        return f"RF Fire Sensor {first_param} Missing"
    if key == "01_0082":
        return f"RF Fire Sensor {first_param} Missing Restore"
    if key == "01_0083":
        return f"RF Receiver Missing"
    if key == "01_0084":
        return f"RF Receiver Missing Restore"
    if key == "01_0085":
        return f"RF Receiver Jamming"
    if key == "01_0086":
        return f"RF Receiver Jamming Restore"
    if key == "01_0087":
        return f"RF Receiver Tamper"
    if key == "01_0088":
        return f"RF Receiver Tamper Restore"
    if key == "01_0089":
        return f"RF Repeater {first_param} Missing"
    if key == "01_0090":
        return f"RF Repeater {first_param} Missing Restore"
    if key == "01_0091":
        return f"RF Repeater Jamming"
    if key == "01_0092":
        return f"RF Repeater Jamming Restore"
    if key == "01_0093":
        return f"RF Repeater {first_param} Tamper"
    if key == "01_0094":
        return f"RF Repeater {first_param} Tamper Restore"
    if key == "01_0095":
        return f"Codepad {first_param} Missing"
    if key == "01_0096":
        return f"Codepad {first_param} Missing Restore"
    if key == "01_0097":
        return f"Codepad {first_param} Tamper"
    if key == "01_0098":
        return f"Codepad {first_param} Tamper Restore"
    if key == "01_0099":
        return f"IP Module {first_param} Missing"
    if key == "01_0100":
        return f"IP Module {first_param} Missing Restore"
    if key == "01_0101":
        return f"IP Module {first_param} Tamper"
    if key == "01_0102":
        return f"IP Module {first_param} Tamper Restore"
    if key == "01_0103":
        return f"Ex. Output {first_param} Missing"
    if key == "01_0104":
        return f"Ex. Output {first_param} Missing Restore"
    if key == "01_0105":
        return f"Ex. Output {first_param} Tamper"
    if key == "01_0106":
        return f"Ex. Output {first_param} Tamper Restore"
    if key == "01_0107":
        return f"Walk Test Begin"
    if key == "01_0108":
        return f"Walk Test End"
    if key == "01_0109":
        return f"Program Change"
    if key == "01_0110_ALink":
        return f"A-Link Set Clock"
    if key == "01_0110_User":
        return f"User{first_param} Set Clock"
    if key == "01_0111":
        return f"Phone Line Fail"
    if key == "01_0112":
        return f"Phone Line Restore"
    if key == "01_0113":
        return f"Warning Device Fail"
    if key == "01_0114":
        return f"Warning Device Restore"
    if key == "01_0115":
        return f"Comm Fail"
    if key == "01_0116":
        return f"Comm Restore"
    if key == "01_0117":
        return f"Comm Manual Test"
    if key == "01_0118":
        return f"Comm Auto Test"
    if key == "01_0119":
        return f"ExInput {first_param} Missing"
    if key == "01_0120":
        return f"ExInput {first_param} Missing Restore"
    if key == "01_0121":
        return f"ExInput {first_param} Tamper"
    if key == "01_0122":
        return f"ExInput {first_param} Tamper Restore"
    if key == "01_0123":
        return f"PUSH FAIL MOD {first_param}"
    if key == "01_0124":
        return f"PUSH RES. MOD {first_param}"
    if key == "99_0000":
        return f"System reset"
    if key == "99_0001":
        return f"Away Arm: area {first_param}"
    if key == "99_0002":
        return f"System disarm"
    if key == "99_0003":
        return f"Panic alarm: area {first_param} zone {second_param}"
    return "Unknown history event"