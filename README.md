# Home assistant integration for solution 3000
This integration allows for connecting home assistant to a solution 2000 or 3000 panel with an IP Module.
It is based on a combination of the [vera integration](https://drive.google.com/file/d/1kbwVQMPxxul9jySapcCZM9C5rQPPKN4k/view) and https://github.com/EHylands/homebridge-boschcontrolpanel_bgseries.

Do note that using this integration will stop both A-Link and the RSC+ app from working, as the panel only accepts connections from one source at a time.

## Configuration
You will need the ip, port, and the user code (the code used for the RSC+ app) for your module

The default port is 7700

![screenshot](screenshot.png)

Note that the alarm does not not have an ability to let home assistant know what type of sensor is in use, but you can customise this from home assitant's ui.

Note that if you get an "Invalid App Passcode" error, this means that the panel has refused authentication. This can happen if another connection is active to the panel, such as a A-Link or RSC+ app being connected to the panel. 
