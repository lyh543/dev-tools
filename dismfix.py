#!/usr/bin/env python3

from __init__ import *

system(
    "DISM /Online /Cleanup-Image /ScanHealth",
    "DISM /Online /Cleanup-Image /RestoreHealth"
)