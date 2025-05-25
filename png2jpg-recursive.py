#!/usr/bin/env python3

import subprocess
import click
from __init__ import *
from lib.log import setup_logger


def png2jpg(input: str, output: str) -> int:
    """
    :param input: input file path
    :param output: output file path
    """
    return subprocess.check_call(["magick", input, output])


def png2jpg_recursive(path="."):
    """
    :param path: directory path
    """
    file_list = traverse(
        path,
        filename_filter=extension_allow_filter(["png", "bmp", "jpg"]),
        dirname_filter=filename_block_filter(COMMON_IGNORED_DIRECTORIES),
    )
    filtered_file_list = list(
        filter(
            lambda f: get_ext(f) != ".jpg" and get_stem(f) + ".jpg" not in file_list,
            file_list,
        )
    )
    output_list = list(map(lambda f: get_stem(f) + ".jpg", filtered_file_list))

    input_output_list = list(zip(filtered_file_list, output_list))
    input_output_str = map(lambda x: " -> ".join(x), input_output_list)
    print("file_list:", "\n".join(input_output_str), sep="\n", end="\n\n")

    for i in range(len(input_output_list)):
        [input, output] = input_output_list[i]
        print(f"[{i + 1}/{len(input_output_list)}]: {input} -> {output}")
        value = png2jpg(input=input, output=output)
        if value == 255:
            exit(value)


@click.command()
@click.argument("path", default=".")
def main(path: str):
    setup_logger()
    png2jpg_recursive(path)


if __name__ == "__main__":
    main()
