#!/usr/bin/env python3

from concurrent.futures import ThreadPoolExecutor
import click
from __init__ import *
from ffmpeg2m import ffmpeg2m
from lib.log import setup_logger


def ffmpeg2m_recursive(path=".", use_gpu: bool = True):
    """
    :param path: directory path
    :param use_gpu: True=use GPU if exists, False=use CPU
    :return: if is exited by Ctrl+C, clean unfinished output and return 255
    """
    file_list = traverse(
        path,
        filename_filter=extension_allow_filter(VIDEO_FILE_EXTENSIONS),
        dirname_filter=filename_block_filter(COMMON_IGNORED_DIRECTORIES),
    )
    filtered_file_list = list(
        filter(
            lambda f: f.split(".")[-2] != "compressed"
            and get_stem(f) + ".compressed.mp4" not in file_list,
            file_list,
        )
    )
    output_list = list(
        map(lambda f: f[: f.rfind(".")] + ".compressed.mp4", filtered_file_list)
    )

    input_output_list = list(zip(filtered_file_list, output_list))
    input_output_str = map(lambda x: " -> ".join(x), input_output_list)
    print("file_list:", "\n".join(input_output_str), sep="\n", end="\n\n")

    def func(input_output):
        [input, output] = input_output
        value = ffmpeg2m(input, output, use_gpu=use_gpu, overwrite="never")
        # TODO: support Ctrl+C, after cleanup of other threads is handled correctly
        # if value in [255, 65280]:
        #     print("exiting")
        #     exit(value)
        # print("\n")
        return value

    with ThreadPoolExecutor(max_workers=4) as executor:
        list(executor.map(func, input_output_list))


@click.command()
@click.option(
    "--use_gpu/--not_use_gpu", is_flag=True, default=True, help="Use GPU if exists"
)
@click.argument("path", default=".")
def main(path: str, use_gpu: bool = True):
    setup_logger()
    ffmpeg2m_recursive(path, use_gpu=use_gpu)


if __name__ == "__main__":
    main()
