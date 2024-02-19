#!/usr/bin/env python3

import click
from __init__ import *
from lib.ffmpeg import ffmpeg, OverwriteOptions
from lib.log import setup_logger


def ffmpeg2m_recursive(path=".", use_gpu: bool = True):
    """
    :param path: directory path
    :param use_gpu: True=use GPU if exists, False=use CPU
    :return: if is exited by Ctrl+C, clean unfinished output and return 255
    """
    file_list = traverse(
        path,
        filename_filter=extension_allow_filter(["ts", "mp4"]),
        dirname_filter=filename_block_filter(COMMON_IGNORED_DIRECTORIES),
    )
    filtered_file_list = list(
        filter(
            lambda f: f.split(".")[-1] == "ts"
            and get_stem(f) + ".ts.mp4" not in file_list,
            file_list,
        )
    )
    output_list = list(map(lambda f: f[: f.rfind(".")] + ".ts.mp4", filtered_file_list))

    input_output_list = list(zip(filtered_file_list, output_list))
    input_output_str = map(lambda x: " -> ".join(x), input_output_list)
    print("file_list:", "\n".join(input_output_str), sep="\n", end="\n\n")
    for i in range(len(input_output_list)):
        [input, output] = input_output_list[i]
        print(f"[{i + 1}/{len(input_output_list)}] ", end="")
        value = ffmpeg(input=input, output=output, copy_mode=True, overwrite="never")
        if value == 255:
            exit(value)
        print("\n")


@click.command()
@click.argument("path", default=".")
def main(path: str):
    setup_logger()
    ffmpeg2m_recursive(path)


if __name__ == "__main__":
    main()
