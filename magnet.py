#!/usr/bin/env python3

from __init__ import *

[btih] = argparse("btih", rest="error")

if len(btih) == 40:
    print('magnet:?xt=urn:btih:' + btih)
    exit(0)
else:
    print("btih should be 40 characters")
    exit(1)
