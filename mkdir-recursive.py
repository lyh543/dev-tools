#!/usr/bin/env python3

import click
from __init__ import *


@click.command()
@click.argument("folder")
def main(folder: str):
    os.makedirs(folder)


if __name__ == "__main__":
    main()
