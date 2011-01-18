#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Manages the Rhythmbox playlist.

Allows the current file being played in Rhythmbox to be added or removed from
any of the playlists available. Also allows to create new playlists.
"""

import os
import dbus
import argparse

from subprocess  import call, Popen, PIPE
from utils       import *


###############################################################################
# Ugly global variables
bus = dbus.SessionBus()

rb = bus.get_object("org.gnome.Rhythmbox"
                   ,"/org/gnome/Rhythmbox/PlaylistManager")
rb = dbus.Interface(rb, "org.gnome.Rhythmbox.PlaylistManager")

player = bus.get_object("org.gnome.Rhythmbox", "/org/gnome/Rhythmbox/Player")
player = dbus.Interface(player, "org.gnome.Rhythmbox.Player")


###############################################################################
# Functions
def parse_arguments():
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument("--create"
                       ,type    = str
                       ,nargs   = "?"
                       ,default = None
                       ,metavar = "NAME"
                       ,help="Creates a playlist as NAME")

    parser.add_argument("--add"
                       ,type    = list
                       ,nargs   = "?"
                       ,default = None
                       ,metavar = "PLAYLISTS"
                       ,help="Adds current song to PLAYLISTS")

    parser.add_argument("--remove"
                       ,type    = list
                       ,nargs   = "?"
                       ,default = None
                       ,metavar = "PLAYLISTS"
                       ,help="Removes current song from PLAYLISTS")

    return parser.parse_args()


# -----------------------------------------------------------------------------
def create(name=None):
    """Creates a new playlist with the given name.

    If ``name`` is ``None``, prompts the user for a name for he playlist.
    """
    if not name:
        name = entry("Playlist name:")
        
    rb.createPlaylist(name)
    

# -----------------------------------------------------------------------------
def add(playlists):
    """Adds the current song to the given playlists.
    """
    if not playlists:
        playlists = get_list(["Playlists"]
                            ,rb.getPlaylists()
                            ,multiple = True
                            ,text     = "Add to playlists:")
    
    song = player.getPlayingUri()
    for playlist in playlists:
        rb.addToPlaylist(playlist, song)


# -----------------------------------------------------------------------------
def remove(playlists):
    """Removes the current song from the given playlists.
    """
    if not playlists:
        playlists = get_list(["Playlists"]
                            ,rb.getPlaylists()
                            ,multiple = True
                            ,text     = "Remove from playlists:")
    
    song = player.getPlayingUri()
    for playlist in playlists:
        rb.removeFromPlaylist(playlist, song)


# -----------------------------------------------------------------------------
def main():
    args = parse_arguments()

    if args.create is not None:
        create(args.create)

    elif args.add is not None:
        add(args.add)

    elif args.remove is not None:
        remove(args.remove)

    else:
        print "buu"


if __name__ == "__main__":
    main()

    
