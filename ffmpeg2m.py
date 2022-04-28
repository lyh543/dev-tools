#!/usr/bin/env python3

from __init__ import *

[input, output] = argparse("input", "output", rest="error")

system(
    f"ffmpeg "
    f"-hwaccel cuda "
    f"-i {input} "
    f"-b:v 2M "
    # -vf scale=-1:720 
    f"-c:v hevc_nvenc "
    f"{output}"
)
