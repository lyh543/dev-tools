#!/usr/bin/env python3

from __init__ import *
from lib.image import *


def clean_uncompressed_recursive(path="."):
    """
    :param path: directory path
    """
    compressed_file_list = traverse(
        path, lambda filename, filepath: ".compressed." in filename
    )

    # replace last occurrence
    def rreplace(s: str, old: str, new: str, occurrence: int):
        li = s.rsplit(old, occurrence)
        return new.join(li)

    uncompressed_file_list = list(
        map(lambda s: rreplace(s, ".compressed.", ".", 1), compressed_file_list)
    )

    existed_uncompressed_file_list = list(
        filter(lambda s: pathlib.Path(s).exists(), uncompressed_file_list)
    )

    print("files to be removed: ")
    print("\n".join(existed_uncompressed_file_list))
    print(f"\n{len(existed_uncompressed_file_list)} in total.")

    if len(existed_uncompressed_file_list) > 0:
        input("Press Enter to remove, Ctrl+C to abort")
        for file in existed_uncompressed_file_list:
            os.remove(file)


if __name__ == "__main__":
    [rest] = argparse(rest="return")
    clean_uncompressed_recursive(".")
