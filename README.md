# Note: This plugin has been deprecated
I have merged this into https://github.com/mag1024/bosch-alarm-homeassistant, as it was just overall a much more stable integration, and it means we can have a single integration for multiple bosch panels.

# Home assistant integration for solution 3000
This integration allows for connecting home assistant to a solution 2000 or 3000 panel with an IP Module.
It is based on a combination of the [vera integration](https://drive.google.com/file/d/1kbwVQMPxxul9jySapcCZM9C5rQPPKN4k/view) and https://github.com/EHylands/homebridge-boschcontrolpanel_bgseries.

Do note that using this integration will stop both A-Link and the RSC+ app from working, as the panel only accepts connections from one source at a time.

## Configuration
You will need the ip, port, and the user code (the code used for the RSC+ app) for your module

The default port is 7700
