#!/usr/bin/env python3

import click
from __init__ import *


@click.command()
@click.argument("btih")
def main(btih: str):
    if len(btih) == 40:
        print("magnet:?xt=urn:btih:" + btih)
        exit(0)
    else:
        print("btih should be 40 characters")
        exit(1)


if __name__ == "__main__":
    main()
