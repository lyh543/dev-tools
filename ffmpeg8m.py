#!/usr/bin/env python3

import click
from __init__ import *
from lib.ffmpeg import ffmpeg, OverwriteOptions
from lib.ffmpeg_utils import get_compressed_output_path
from lib.log import setup_logger


def ffmpeg8m(
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
        video_bitrate="8M",
        audio_bitrate="128K",
        drop_duplicate_frames=True,
    )


@click.command()
@click.option(
    "--not_use_gpu", "use_gpu", is_flag=True, default=True, help="Do not use GPU"
)
@click.argument("input")
@click.argument("output", default="")
def main(input: str, output: str, use_gpu: bool = True):
    setup_logger()
    if not output:
        output = get_compressed_output_path(input)
    ffmpeg8m(input, output, use_gpu=use_gpu)


if __name__ == "__main__":
    main()
