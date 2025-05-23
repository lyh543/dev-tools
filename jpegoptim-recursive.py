#!/usr/bin/env python3

import os
import subprocess
import shutil
import click
from __init__ import *
from lib.image import *


def jpegoptim_recursive(
    height: int = None, width: int = None, size: int = 1000, path="."
):
    """
    Recursively compress images in the given directory and its subdirectories.
    :param height: target height of the image, e.g. 1080
    :param width: target width of the image, e.g. 1080
    :param size: target size of the image in KB, e.g. 1000
    :param path: directory path
    """
    file_list = traverse(
        path,
        filename_filter=extension_allow_filter(IMAGE_FILE_EXTENSIONS),
        dirname_filter=filename_block_filter(COMMON_IGNORED_DIRECTORIES),
    )

    filtered_file_list = list(
        filter(
            lambda f: f.split(".")[-2] != "compressed"
            and get_stem(f) + ".compressed.jpg" not in file_list,
            file_list,
        )
    )
    output_list = list(
        map(lambda f: f[: f.rfind(".")] + ".compressed.jpg", filtered_file_list)
    )

    input_output_list = list(zip(filtered_file_list, output_list))
    input_output_str = map(lambda x: " -> ".join(x), input_output_list)
    print("file_list:", "\n".join(input_output_str), sep="\n", end="\n\n")
    for i in range(len(input_output_list)):
        [input, output] = input_output_list[i]
        print(f"[{i + 1}/{len(input_output_list)}] ", end="")

        try:
            # Resize the image if height and width are provided
            if height is not None or width is not None:
                resize_args = []
                if height:
                    resize_args.append(f"{height}")
                else:
                    resize_args.append("")
                if width:
                    resize_args.append(f"x{width}")
                else:
                    resize_args.append("x")
                resize_str = "".join(resize_args)

                subprocess.run(
                    ["magick", input, "-resize", resize_str, output],
                    check=True,
                )
            else:
                shutil.copy(input, output)

            # Compress the image to the target size
            subprocess.run(
                ["magick", output, "-define", f"jpeg:extent={size}KB", output],
                check=True,
            )
        except subprocess.CalledProcessError as e:
            print(f"Error processing {input}: {e}")
            if os.path.exists(output):
                os.remove(output)
            exit(1)

        print("\n")


@click.command()
@click.option(
    "--height", default=None, help="target height of the image, e.g. 1080", type=int
)
@click.option(
    "--width", default=None, help="target width of the image, e.g. 1080", type=int
)
@click.option(
    "--size", default=1000, help="target size of the image in KB, e.g. 1000", type=int
)
@click.argument("path", default=".")
def main(path: str, height: int, width: int, size: int):
    jpegoptim_recursive(height=height, width=width, size=size, path=path)


if __name__ == "__main__":
    main()
