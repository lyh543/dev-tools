#!/usr/bin/env python3

from __init__ import *

[msg, rest] = argparse("msg", rest="return")

system(
    "git add --all",
    f'git commit --amend -m "{msg}" {rest}'
)
