#!/usr/bin/env python3

from __init__ import *

[path] = argparse("path", rest="error")

system(
    rf'Import-Module "$env:ChocolateyInstall\helpers\chocolateyInstaller.psm1"',
    rf'Install-ChocolateyPath {path}',
    rf'echo success',
    run_pwsh_on_win=True,
)
