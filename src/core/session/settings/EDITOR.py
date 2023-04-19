"""
Set attacker's prefered text editor.

* USE CASES:

# open TARGET setting content with EDITOR:
> set TARGET +

# use `edit` plugin to edit a remote file locally with EDITOR:
> edit /var/www/html/index.php
"""
import os
import linebuf
import datatypes


linebuf_type = linebuf.MultiLineBuffer


def validator(value):
    return datatypes.ShellCmd(value)


def default_value():
    return os.environ.get("EDITOR", "vi")
