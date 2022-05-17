#!/usr/bin/env python3
from time import sleep
from typing import Optional

from __init__ import *


def ffmpeg2m(input: str, output: str, overwrite: Optional[bool] = None):
    """
    :param input: input file path
    :param output: output file path
    :param overwrite: True=always overwrite, False=never overwrite, None=ask
    :return: exit code. if is exited by Ctrl+C, clean unfinished output and return 255
    """
    overwrite_option = '-y' if overwrite is True \
        else '-n' if overwrite is False \
        else ''
    command = (f"ffmpeg "
               f"{overwrite_option} "
               f"-hwaccel cuda "
               f'-i "{input}" '
               f"-b:v 2M "
               # -vf scale=-1:720 \ 
               f"-c:v hevc_nvenc "
               f'"{output}"')
    print('\n\n>>>', command)
    # catch ctrl+c
    try:
        value = system(command, exit_on_errors=False)
    except KeyboardInterrupt:
        value = 255

    if value == 255:
        print(f'cleanup (remove {output})...')
        sleep(0.5)
        try:
            os.remove(output)
        except FileNotFoundError:
            pass
        return value


if __name__ == '__main__':
    [input, output] = argparse("input", "output", rest="error")
    exit(ffmpeg2m(input, output))
