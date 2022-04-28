#!/usr/bin/env python3

from __init__ import *

[rest] = argparse(rest="return")

if isWindows:
    system("wsl ls -lh " + rest)
else:
    system("wsl ls -lh " + rest)