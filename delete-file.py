#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2010 Quildreen Motta
# Released under the MIT licence

"""Deletes the current file being played in Rhythmbox.
"""

import os
import sys
import dbus
import argparse

from subprocess import call
from utils      import sanitize, notify


def can_remove(filename):
    """Asks the user whether the given filename should be removed.
    """
    cmd = ["zenity", "--question", "--title", "Delete this file?"
          ,"--text", filename]
    return call(cmd) == 0


def parse_arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()


def main():
    parse_arguments()

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
