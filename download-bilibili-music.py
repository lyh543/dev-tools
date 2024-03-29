import tempfile
import logging
import shutil
import re
import os
import pathlib
from bs4 import BeautifulSoup

import click
import requests

from __init__ import *
from lib.ffmpeg import ffmpeg
from lib.log import setup_logger

BROWSER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}


def clean_filename(name: str) -> str:
    return re.sub(r"[\/\\\:\*\?\"\<\>\|]", "_", name)


def parse_bv_from_url(url: str) -> str:
    re_search_result = re.search(r"BV(\w+)", url)
    return re_search_result.group(1)


def get_bilibili_video_title(url: str) -> str:
    response = requests.get(url, headers=BROWSER_HEADERS)
    try:
        title = BeautifulSoup(response.text, features="lxml").title.string
        logging.info(f"Title: {title}")
        return title
    except AttributeError:
        bv = parse_bv_from_url(url)
        logging.warning(f"Cannot find title in response text, use BV: {bv}")
        return bv


def download_bilibili_video(url: str, save_dir: pathlib.Path, name: str):
    os.system(f"you-get -o {save_dir} -O {name} {url}")


@click.command()
@click.option("--temp_dir", default=None, help="temp dir to save video")
@click.argument("bv_or_url")
def main(bv_or_url: str, temp_dir: str):
    """
    BV_OR_URL: bilibili video bv (BV1gb4y1n7rQ) or url (https://www.bilibili.com/video/BV1gb4y1n7rQ)
    """
    setup_logger()
    if bv_or_url.lower().startswith("bv"):
        bv = bv_or_url
        url = f"https://www.bilibili.com/video/{bv}/"
    else:
        url = bv_or_url
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
    logging.info(f"Done! {clean_title}.mp3")


if __name__ == "__main__":
    main()
