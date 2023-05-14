from __init__ import *
from lib.ffmpeg import ffmpeg
import requests
import re
import os
import pathlib

TITLE_REGEXP = re.compile(r"<title.*?>(.*)_哔哩哔哩_bilibili</title>")


def get_bilibli_url(bv: str) -> str:
    return f"https://www.bilibili.com/video/{bv}"


def get_bilibili_video_title(bv: str) -> str:
    url = get_bilibli_url(bv)
    response = requests.get(url)
    re_search_result = re.search(TITLE_REGEXP, response.text)
    return re_search_result.group(1)


def download_bilibili_video(bv: str, save_dir: pathlib.Path, name: str):
    url = get_bilibli_url(bv)
    os.system(f"you-get -o {save_dir} -O {name} {url}")


if __name__ == "__main__":
    [bv] = argparse(["bv"], rest="error")
    save_dir = pathlib.Path.cwd()
    video_path = save_dir / f"{bv}.mp4"
    music_path = save_dir / f"{bv}.mp3"

    title = get_bilibili_video_title(bv)
    download_bilibili_video(bv, save_dir, bv)
    ffmpeg(
        str(video_path),
        str(music_path),
        use_gpu=False,
        overwrite="always",
        audio_bitrate="256K",
    )
    music_path.rename(music_path.parent / f"{title}.mp3")
    print(f"Done! {title}.mp3")
