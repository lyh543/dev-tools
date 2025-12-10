#!/usr/bin/env python3

from __init__ import *

system('ssh root@192.168.6.1 "/usr/bin/wol -v -i 192.168.6.255 2c:f0:5d:27:5c:91"')
