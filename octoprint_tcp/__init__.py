# coding=utf-8
from __future__ import absolute_import
import serial
import octoprint.plugin
from octoprint.util.comm import BufferedReadlineWrapper

class TcpPlugin(octoprint.plugin.SettingsPlugin,
                octoprint.plugin.AssetPlugin,
                octoprint.plugin.TemplatePlugin
                ):
    ##~~ SettingsPlugin mixin
    def get_settings_defaults(self):
        return {
            "enabled": False,
            "remote_host": "192.168.xx.xx",
            "remote_port": 23,
        }

    def get_template_vars(self):
        template_vars = super().get_template_vars()
        template_vars["enabled"] = self._settings.get(["enabled"])
        template_vars["remote_host"] = self._settings.get(["remote_host"])
        template_vars["remote_port"] = self._settings.get(["remote_port"])
        return template_vars

    def get_template_configs(self):
        return [
            dict(type="settings", custom_bindings=False),
        ]

    def get_additional_port_names(self, *args, **kwargs):
        if self._settings.get_boolean(["enabled"]):
            return ["TCP"]
        else:
            return []

    def virtual_serial_factory(self, comm_instance, port, baudrate, read_timeout):
        if not port == "TCP":
            return None

        if not self._settings.get_boolean(["enabled"]):
            return None

        import logging.handlers

        from octoprint.logging.handlers import CleaningTimedRotatingFileHandler

        seriallog_handler = CleaningTimedRotatingFileHandler(
            self._settings.get_plugin_logfile_path(postfix="serial"),
            when="D",
            backupCount=3,
        )
        seriallog_handler.setFormatter(logging.Formatter("%(asctime)s %(message)s"))
        seriallog_handler.setLevel(logging.DEBUG)

        remote_host = self._settings.get(["remote_host"])
        remote_port = self._settings.get(["remote_port"])
        url = f"socket://{remote_host}:{remote_port}"
        self._logger.info(f"Connecting to {url}...")
        serial_obj = serial.serial_for_url(url, do_not_open=True)
        try:
            serial_obj.open()
        except serial.SerialException:
            self._logger.info(
                f"Failed to connect: {url} did not respond."
            )
            return None

        return serial_obj

    ##~~ AssetPlugin mixin

    def get_assets(self):
        # Define your plugin's asset files to automatically include in the
        # core UI here.
        return {
            "js": ["js/tcp.js"],
            "css": ["css/tcp.css"],
            "less": ["less/tcp.less"]
        }

    ##~~ Softwareupdate hook

    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
        # for details.
        return {
            "tcp": {
                "displayName": "TCP",
                "displayVersion": self._plugin_version,

                # version check: GitHub repository
                "type": "github_release",
                "user": "jake5253",
                "repo": "OctoPrint-Tcp",
                "current": self._plugin_version,

                # update method: pip
                "pip": "https://github.com/jake5253/OctoPrint-Tcp/archive/{target_version}.zip",
            }
        }


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Tcp Plugin"

# Set the Python version your plugin is compatible with below. Recommended is Python 3 only for all new plugins.
# OctoPrint 1.4.0 - 1.7.x run under both Python 3 and the end-of-life Python 2.
# OctoPrint 1.8.0 onwards only supports Python 3.
__plugin_pythoncompat__ = ">=3,<4"  # Only Python 3


def __plugin_load__():
    plugin = TcpPlugin()

    global __plugin_implementation__
    __plugin_implementation__ = plugin

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": plugin.get_update_information,
        "octoprint.comm.transport.serial.additional_port_names": plugin.get_additional_port_names,
        "octoprint.comm.transport.serial.factory": plugin.virtual_serial_factory
    }
