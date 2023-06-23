#!/usr/bin/env python3

import click
from __init__ import *


@click.command()
@click.argument("path")
def main(path: str):
    if isWindows:
        system(
            rf'Import-Module "$env:ChocolateyInstall\helpers\chocolateyInstaller.psm1"',
            rf"Install-ChocolateyPath {path}",
            rf'echo if you don\'t see anything like "adding it", the command may fail',
            run_pwsh_on_win=True,
        )
    else:
        raise NotImplementedError()


if __name__ == "__main__":
    main()
