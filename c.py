#!/usr/bin/env python3

import click
from __init__ import *


@click.command(
    context_settings=dict(
        ignore_unknown_options=True,
    )
)
@click.argument("msg")
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def main(msg: str, args: List[str]):
    print(args)
    system(f"git add --all", f'git commit -m "{msg}" {" ".join(args)}')


if __name__ == "__main__":
    main()
