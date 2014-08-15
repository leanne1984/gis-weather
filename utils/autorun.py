#!/usr/bin/env python3

#  A simple crossplatform autostart helper
#  by Jonas Wagner

from __future__ import with_statement

import os
import sys

if sys.platform == 'win32':
    import winreg
    _registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
    def get_runonce():
        return winreg.OpenKey(_registry,
                r"Software\Microsoft\Windows\CurrentVersion\Run", 0,
        winreg.KEY_ALL_ACCESS)

    def add(name, application):
        """add a new autostart entry"""
        key = get_runonce()
        winreg.SetValueEx(key, name, 0, winreg.REG_SZ, application)
        winreg.CloseKey(key)

    def exists(name):
        """check if an autostart entry exists"""
        key = get_runonce()
        exists = True
        try:
            winreg.QueryValueEx(key, name)
        except WindowsError:
            exists = False
        winreg.CloseKey(key)
        return exists

    def remove(name):
        """delete an autostart entry"""
        key = get_runonce()
        winreg.DeleteValue(key, name)
        winreg.CloseKey(key)
else:
    _xdg_config_home = os.environ.get("XDG_CONFIG_HOME", "~/.config")
    _xdg_user_autostart = os.path.join(os.path.expanduser(_xdg_config_home),
            "autostart")

    def getfilename(name):
        """get the filename of an autostart (.desktop) file"""
        return os.path.join(_xdg_user_autostart, name + ".desktop")

    def add(name, application, delay_start_time):
        """add a new autostart entry"""
        delay = ''
        end = ""
        if delay_start_time != 0:
            delay = "sh -c 'sleep %s; "%delay_start_time
            end = "'"
        desktop_entry = "[Desktop Entry]\n"\
            "Name=%s\n"\
            "Exec=%spython3 \"%s\"%s\n"\
            "Type=Application\n"\
            "Terminal=false\n"\
            "Icon=%s\n"\
            "Comment=%s" % ('Gis Weather', delay, application, end, os.path.join(os.path.dirname(application),'icon.png'), _("Weather widget"))
        with open(getfilename(name), "w") as f:
            f.write(desktop_entry)

    def exists(name):
        """check if an autostart entry exists"""
        return os.path.exists(getfilename(name))

    def remove(name):
        """delete an autostart entry"""
        os.unlink(getfilename(name))
