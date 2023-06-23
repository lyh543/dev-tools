#!/usr/bin/env python3

import click
from __init__ import *


@click.command()
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def main(args: List[str]):
    system("exa  --icons -lh " + " ".join(args))


if __name__ == "__main__":
    main()
