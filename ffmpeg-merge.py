#!/usr/bin/env python3
import tempfile

import click

from __init__ import *


def print_and_run_command(command: str) -> None:
    print(">>>", command)
    system(command)


def ffmpeg_slice(input_list: list[str]) -> int:
    slice_list_filepath = tempfile.mktemp(suffix=".slice.temp.txt")
    output_path = f"{input_list[0]}.slice.mp4"
    print(f'Created slice list file "{slice_list_filepath}"')

    with open(slice_list_filepath, "w") as slice_list_file:
        for input in input_list:
            slice_list_file.write(f"file '{os.path.abspath(input)}'\n")

    print_and_run_command(
        f'ffmpeg -y -f concat -safe 0 -i "{slice_list_filepath}" -c:v copy -c:a copy "{output_path}"'
    )
    print(f'Successfully merged files into "{output_path}"')

    pathlib.Path(slice_list_filepath).unlink()


@click.command()
@click.argument("input", nargs=-1)
def main(input: List[str]) -> None:
    ffmpeg_slice(input)


if __name__ == "__main__":
    main()
