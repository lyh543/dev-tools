import click
from __init__ import *
from lib.ffmpeg import ffmpeg
import pathlib


@click.command()
@click.argument("video_path")
def main(video_path: str):
    extension = pathlib.Path(video_path).suffix
    music_path = video_path.replace(extension, ".mp3")
    ffmpeg(
        str(video_path),
        str(music_path),
        use_gpu=False,
        overwrite="always",
        audio_bitrate="256K",
    )
    print(f"Done! {music_path}")


if __name__ == "__main__":
    main()
