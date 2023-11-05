import tempfile
import logging
import shutil
import re
import os
import pathlib

import click
import requests

from __init__ import *
from lib.ffmpeg import ffmpeg
from lib.log import setup_logger

TITLE_REGEXP = re.compile(r"<title.*?>(.*)_哔哩哔哩_bilibili</title>")


def clean_filename(name: str) -> str:
    return re.sub(r"[\/\\\:\*\?\"\<\>\|]", "_", name)


def parse_bv_from_url(url: str) -> str:
    re_search_result = re.search(r"BV(\w+)", url)
    return re_search_result.group(1)


def get_bilibili_video_title(url: str) -> str:
    response = requests.get(url)
    try:
        re_search_result = re.search(TITLE_REGEXP, response.text)
        return re_search_result.group(1)
    except AttributeError:
        bv = parse_bv_from_url(url)
        logging.warning(f"Cannot find title in response text, use BV: {bv}")
        return bv



def download_bilibili_video(url: str, save_dir: pathlib.Path, name: str):
    os.system(f"you-get -o {save_dir} -O {name} {url}")


@click.command()
@click.option("--temp_dir", default=None, help="temp dir to save video")
@click.argument("url")
def main(url: str, temp_dir: str):
    setup_logger()
    bv = parse_bv_from_url(url)
    save_dir = pathlib.Path(
        temp_dir if temp_dir else tempfile.TemporaryDirectory().name
    )
    video_path = save_dir / f"{bv}.mp4"
    music_path = save_dir / f"{bv}.mp3"

    title = get_bilibili_video_title(url)
    clean_title = clean_filename(title)
    download_bilibili_video(url, save_dir, bv)
    ffmpeg(
        str(video_path),
        str(music_path),
        use_gpu=False,
        overwrite="always",
        audio_bitrate="256K",
    )
    shutil.move(music_path, f"{clean_title}.mp3")
    print(f"Done! {clean_title}.mp3")


if __name__ == "__main__":
    main()
