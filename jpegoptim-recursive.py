#!/usr/bin/env python3

from __init__ import *
from lib.image import *


def jpegoptim_recursive(path="."):
    """
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
        value = image_resize(input, output, [1080, -1])
        if value != 0:
            os.remove(output)
            exit(value)
        value = image_compress(output, 100)
        if value != 0:
            os.remove(output)
            exit(value)
        print("\n")


if __name__ == "__main__":
    [rest] = argparse(rest="return")
    jpegoptim_recursive(".")
