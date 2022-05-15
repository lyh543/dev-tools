#!/usr/bin/env python3

import subprocess
import re
from __init__ import *

# https://docs.docker.com/engine/reference/commandline/ps/#formatting
command = 'docker ps --format "table {{.Names}}\t{{.Ports}}"'
result = subprocess.check_output(command, shell=True, text=True)

result = re.sub(r'0.0.0.0:', '0:', result)
# remove ipv6 ports since it's too long
result = re.sub(r':::.*?, ', '', result)
result = re.sub(r':::.*?\n', '\n', result)
print(result)