#!/usr/bin/env python3

from __init__ import *

[filename] = argparse("filename", rest="error")

if isWindows:
    system(f"certutil -hashfile {filename} MD5")
else:
    system(f"md5sum {filename}")