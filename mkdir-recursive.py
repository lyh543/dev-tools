#!/usr/bin/env python3

from __init__ import *

[folder] = argparse("folder", rest="error")

os.makedirs(folder)

# system(
#     f"New-Item {folder} -ItemType Directory"
#     if isWindows
#     else f"mkdir -p {folder}"
# )
