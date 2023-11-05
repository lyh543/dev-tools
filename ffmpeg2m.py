#!/usr/bin/env python3

import click
from __init__ import *
from lib.ffmpeg import ffmpeg, OverwriteOptions
from lib.log import setup_logger


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


@click.command()
@click.option("--use_gpu", is_flag=True, default=True, help="Use GPU if exists")
@click.argument("input")
@click.argument("output")
def main(input: str, output: str, use_gpu: bool = True):
    setup_logger()
    ffmpeg2m(input, output, use_gpu=use_gpu)


if __name__ == "__main__":
    main()
