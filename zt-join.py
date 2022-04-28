#!/usr/bin/env python3

from __init__ import *

system(
    "zerotier-cli join a0cbf4b62a3b4b3f",
    "zerotier-cli orbit 0000007972fedca9 0000007972fedca9",
    "zerotier-cli peers"
)
print("Please go to https://my.zerotier.com/network/a0cbf4b62a3b4b3f to authorize the device.")
