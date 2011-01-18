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
        cmd.append("--title=%s" % (title,))

    return call(cmd) == 0


def entry(prompt, default="", password=False, title=None):
    """Prompts the user to enter some information on a textbox.
    """
    cmd = ["zenity", "--entry", "--text=%s" % (prompt,)
          ,"--entry-text=%s" % (default,)]
    if password:
        cmd.append("--hide-text")
    if title is not None:
        cmd.append("--title=%s" % (title,))

    proc = Popen(cmd, stdout=PIPE)
    proc.wait()
    return proc.communicate()[0].strip()


def get_list(columns, *args, **kwargs):
    """Prompts the user to select values in a list.
    """
    title    = kwargs.pop("title", None)
    text     = kwargs.pop("text", None)
    multiple = kwargs.pop("multiple", False)
    kind     = kwargs.pop("kind", None)

    cmd = ["zenity", "--list", "--separator=\\n"]

    if text is not None:
        cmd.append("--text=%s" % (text,))
    if title is not None:
        cmd.append("--title=%s" % (title,))
    if multiple:
        cmd.append("--multiple")

    if kind == "--checklist":
        cmd.append("--checklist")
    if kind == "--radiolist":
        cmd.append("--radiolist")


    for column in columns:
        cmd.append("--column=%s" % (column,))

    for data in args:
        cmd.extend(data)

    proc = Popen(cmd, stdout=PIPE)
    proc.wait()
    output = proc.communicate()[0]
    
    if output is not None:
        return output.strip().splitlines()
        
    return []
