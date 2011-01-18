# -*- coding: utf-8 -*-
#
# Copyright (c) 2010 Quildreen Motta
# Released under the MIT licence

"""Utilities for rhythmbox dbus scripts.
"""

import urllib

from subprocess import call, Popen, PIPE


def sanitize(uri):
    """Sanitizes the given URI to a local filename
    """
    return urllib.unquote(uri).replace("file://", "")
    

def notify(summary, text, icon=None):
    """Notifies the user through libnotify
    """
    cmd = ["notify-send", summary, text]
    if icon is not None:
        cmd.extend(["-i", icon])

    call(cmd)


def confirm(prompt, title=None):
    """Prompts the user for confirmation.
    """
    cmd = ["zenity", "--question", "--text=%s" % (prompt,)]
    if title is not None:
        cmd.extend(["--title", title])

    return call(cmd) == 0


def entry(prompt, default="", password=False):
    """Prompts the user to enter some information on a textbox.
    """
    cmd = ["zenity", "--entry", "--text=%s" % (prompt,)
          ,"--entry-text=%s" % (default,)]
    if password:
        cmd.append("--hide-text")
    
    proc = Popen(cmd, stdout=PIPE)
    proc.wait()
    return proc.communicate()[0].strip()


