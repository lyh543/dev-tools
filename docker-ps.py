#!/usr/bin/env python3

from __init__ import *

# https://docs.docker.com/engine/reference/commandline/ps/#formatting
system(
    'docker ps --format "table {{.ID}}\t{{.Image}}\t{{.Status}}\t{{.Size}}\t{{.Names}}"',
)
