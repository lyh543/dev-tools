#!/usr/bin/env python3
import traceback
from typing import Tuple

import click

from __init__ import *


def print_and_run_command(command: str) -> None:
    print(">>>", command)
    system(command)


def ffmpeg_slice(input_name: str, time_range_list: List[Tuple[str, str]]) -> int:
    steps = len(time_range_list) + 2
    stem = get_stem(input_name)
    slice_list_filename = stem + ".slice.temp.txt"

    with open(slice_list_filename, "w") as slice_list_file:
        for i, (start, end) in enumerate(time_range_list):
            print(f"\n[{i + 1}/{steps}]: slicing {time_range_list[i]}...")
            output_name = f"{stem}.slice.temp.{i + 1}.mp4"
            print_and_run_command(
                f'ffmpeg -y -i "{input_name}" -ss {start} -to {end} -c:v copy -c:a copy {output_name}'
            )
            slice_list_file.write(f"file '{output_name}'\n")

    print(f"\n[{steps - 1}/{steps}]: merging...")
    print_and_run_command(
        f"ffmpeg -y -f concat -safe 0 -i {slice_list_filename} -c:v copy -c:a copy {stem}.slice.mp4"
    )

    print(f"\n[{steps}/{steps}]: cleaning temp files...")
    for i in range(steps - 2):
        pathlib.Path(f"{stem}.slice.temp.{i + 1}.mp4").unlink()
    pathlib.Path(slice_list_filename).unlink()


@click.command()
@click.argument("input")
@click.argument("time_range", nargs=-1)
def main(input: str, time_range: List[str]) -> None:
    try:
        time_range_list = [range.split("-") for range in time_range]
        for i in range(len(time_range_list)):
            print(f"Slice {i + 1}: {time_range_list[i]} ")
        ffmpeg_slice(input, time_range_list)
    except Exception as e:
        traceback.print_exc()
        print("Usage: ffmpeg-slice.py <input> [hh:mm:ss-hh:mm:ss] [hh:mm:ss-hh:mm:ss]")


if __name__ == "__main__":
    main()
