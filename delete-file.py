#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import dbus
import urllib

from subprocess import call


def sanitize(uri):
    """Sanitizes the given URI to a local filename
    """
    return urllib.unquote(uri).replace("file://", "")
    

def can_remove(filename):
    """Asks the user whether the given filename should be removed.
    """
    cmd = ["zenity", "--question", "--title", "Delete this file?"
          ,"--text", filename]
    return call(cmd) == 0


def notify(summary, text, icon=None):
    """Notifies the user through libnotify
    """
    cmd = ["notify-send", summary, text]
    if icon is not None:
        cmd.extend(["-i", icon])

    call(cmd)


def main():
    # Gets the Rhythmbox player from DBus
    bus = dbus.SessionBus()
    obj = bus.get_object("org.gnome.Rhythmbox", "/org/gnome/Rhythmbox/Player")
    player = dbus.Interface(obj, "org.gnome.Rhythmbox.Player")

    filename = sanitize(player.getPlayingUri())

    # Prompts user for confirmation on removing the file
    if can_remove(filename):
        player.next()
        call(["rm", filename])
        notify("Removed", "\"" + filename + "\"", icon="user-trash-full")


# calls the main routine
if __name__ == "__main__":
    main()
