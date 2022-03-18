import asyncio
from solutions3000 import Panel, UserType, ArmType

async def client():
    panel = Panel(7700, 'ip', UserType.InstallerApp, 'automationcode', 'alink code')
    await panel.initialise()
    await panel.update_status()
    # panel.arm(ArmType.Stay, panel.areas)
    print(panel)

asyncio.run(client())