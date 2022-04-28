#!/usr/bin/env python3

from __init__ import *

[msg, rest] = argparse("msg", rest="return")

system(
    f"git add --all",
    f'git commit -m "{msg}" {rest}'
)
