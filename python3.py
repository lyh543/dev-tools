#!/usr/bin/env python3

from __init__ import *
from datetime import datetime

system(
    "pushd ~/git/bitme",
    f"{PYTHON_EXECUTABLE} replace.py pull",
    "popd",
    run_pwsh_on_win=True,
)
