from solutions3000 import Panel, UserType, ArmType
panel = Panel(7700, 'ip', UserType.InstallerApp, 'automationcode', 'alink code')
panel.initialise()
panel.update_status()
panel.arm(ArmType.Stay, panel.areas)
print(panel)