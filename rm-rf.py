#!/usr/bin/env python3

from __init__ import *

files = sys.argv[1:]

if isWindows:
    for file in files:
        system(
            f'Remove-Item "{file}" -Force -Confirm:$false -Recurse && Write-Output "Successfully remove {file}"',
            run_pwsh_on_win=True,
        )
else:
    system(f"rm -rf {shlex.join(files)}")
