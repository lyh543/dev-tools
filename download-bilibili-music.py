import click
from __init__ import *
from lib.ffmpeg import ffmpeg
import requests
import re
import os
import pathlib

TITLE_REGEXP = re.compile(r"<title.*?>(.*)_哔哩哔哩_bilibili</title>")


def clean_filename(name: str) -> str:
    return re.sub(r"[\/\\\:\*\?\"\<\>\|]", "_", name)


def parse_bv_from_url(url: str) -> str:
    re_search_result = re.search(r"BV(\w+)", url)
    return re_search_result.group(1)


def get_bilibili_video_title(url: str) -> str:
    response = requests.get(url)
    re_search_result = re.search(TITLE_REGEXP, response.text)
    return re_search_result.group(1)


def download_bilibili_video(url: str, save_dir: pathlib.Path, name: str):
    os.system(f"you-get -o {save_dir} -O {name} {url}")


@click.command()
@click.argument("url")
def main(url: str):
    bv = parse_bv_from_url(url)
    save_dir = pathlib.Path.cwd()
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
    music_path.rename(music_path.parent / f"{clean_title}.mp3")
    print(f"Done! {clean_title}.mp3")


if __name__ == "__main__":
    main()
