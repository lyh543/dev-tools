#!/usr/bin/env python3

import logging
import click
from __init__ import *
from lib.log import setup_logger


@click.command()
@click.argument("path")
def main(path: str):
    setup_logger()
    if isWindows:
        system("rundll32 sysdm.cpl,EditEnvironmentVariables")
    else:
        raise NotImplementedError()


if __name__ == "__main__":
    main()
