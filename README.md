# OctoPrint-Tcp

This plugin allows you to connect to your printer via TCP - like socat/ser2net.
It should be noted that this plugin does NOT monitor the serial connection to the PRINTER
it only facilitates the connection to the TCP server.  If you have crappy/connection-dropping wifi, expect problems.

For information about setting up a TCP serial connection, check out [ESPEasy](https://github.com/letscontrolit/ESPEasy) which let's you use an ESP32 or ESP8266 (NodeMCU) to connect to your printer over wifi. See [Serial Server](https://espeasy.readthedocs.io/en/latest/Plugin/P020.html) for more info about that plugin.

NOTE: May require soldering and/or modifying the printer controller. Do this at your own risk. I am not responsible for any damage to your printer.

Other options include RPi Pico or probably any device that has wifi and supports MicroPython (search for "MicroPython telnet server" may yield something useful? untested).

This plugin comes with no warranty. You should assume it will destroy your 3d printer and make your cat sick or worse. Use at your own risk.

## Setup

Install via the bundled [Plugin Manager](https://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html)
or manually using this URL:

    https://github.com/jake5253/OctoPrint-Tcp/archive/master.zip

## Configuration

Once you have a functional serial server and you've installed this plugin, go into OctoPrint settings, TCP Plugin, and enable it. Fill in the IP address and port of your serial server. Profit!


Please also note: This plugin works for me. I've tested it extensively (I printed something that took about 38 minutes start to finish) and ran into no issues. If you run into any issues, please [open an issue](https://github.com/jake5253/OctoPrint-Tcp/issues) and let me know. I won't promise anything but we'll see how it goes. Pull request if you like.