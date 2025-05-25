#!/usr/bin/env python3

import sys
from __init__ import *
from datetime import datetime

system(
    "python",
    *sys.argv[1:],
    run_pwsh_on_win=True,
)
