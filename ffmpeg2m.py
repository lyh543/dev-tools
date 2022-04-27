#!/usr/bin/env python3

from __init__ import *

[input, output] = argparse("input", "output", rest="error")

system("ffmpeg "
       "-hwaccel cuda "
       f"-i {input} "
       "-b:v 2M "
       # -vf scale=-1:720 
       "-c:v hevc_nvenc "
       f"{output}"
       )
