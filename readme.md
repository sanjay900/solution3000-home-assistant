# Home assistant integration for solutions 3000
This integration is a work in progress for connecting home assistant to a solutions 3000 (and possibly 2000) panel.
It is based on a combination of the [vera integration](https://drive.google.com/file/d/1kbwVQMPxxul9jySapcCZM9C5rQPPKN4k/view) and https://github.com/EHylands/homebridge-boschcontrolpanel_bgseries.

## Configuration
You will need the ip, port, automation password and the installer code for your module
The automation password can be found via A-Link. It will be under the config via the "Comm\Network Config\A-Link/RSC Password" option under A-Link, and the installer code is found under "Access\Installer Code" option.
The default port is 7700
The default installer code is 1234, but this will likley have been changed by your installer
The default automation password is 0000000000
