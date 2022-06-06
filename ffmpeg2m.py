#!/usr/bin/env python3
from time import sleep
from typing import Optional

from __init__ import *
from lib.ffmpeg import ffmpeg, OverwriteOptions


def ffmpeg2m(
    input: str, output: str, use_gpu: bool = True, overwrite: OverwriteOptions = "ask"
) -> int:
    """
    :param input: input file path
    :param output: output file path
    :param use_gpu: True=use GPU if exists, False=use CPU
    :param overwrite: "always" "never" "ask"
    :return: exit code. if is exited by Ctrl+C, clean unfinished output and return 255
    """
    return ffmpeg(
        input=input,
        output=output,
        use_gpu=use_gpu,
        overwrite=overwrite,
        video_bitrate="2M",
        audio_bitrate="128K",
        resolution=[-1, 1080],
    )


if __name__ == "__main__":
    [input, output] = argparse("input", "output", rest="error")
    exit(ffmpeg2m(input, output))
