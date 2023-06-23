#!/usr/bin/env python3

import click
from __init__ import *


@click.command()
@click.argument("name")
def main(name: str):
    if isWindows:
        system("where.exe " + name)
    else:
        system("whereis " + name)


if __name__ == "__main__":
    main()
