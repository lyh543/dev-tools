#!/usr/bin/env python3

from __init__ import *

[rest] = argparse(rest="return")

if isWindows:
    system("where.exe " + rest)
else:
    system("whereis " + rest)
