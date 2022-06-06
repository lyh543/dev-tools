from time import sleep
from typing import List, Literal

from .system_specific import *

OverwriteOptions = Literal["always", "never", "ask"]
GpuOptions = Literal["nvidia", "amd", "no_gpu", None]


def ffmpeg(
    input: str,
    output: str,
    use_gpu: bool = True,
    overwrite: OverwriteOptions = "ask",
    video_bitrate: str = None,
    audio_bitrate: str = None,
    resolution: [int, int] = None,
):
    """
    run ffmpeg command

    :param input: input file path e.g. "input.mov"
    :param output: output file path e.g. "output.mp4"
    :param use_gpu: True=use GPU if exists, False=use CPU
    :param overwrite: "always" "never" "ask"
    :param video_bitrate: e.g. "2M" for 2Mbps
    :param audio_bitrate: e.g. "128K" for 128Kbps
    :param resolution: [width, height] e.g. [-1, 720] for auto:720p
    :return: command to run
    """
    command = FFmpeg.ffmpeg_command(
        input=input,
        output=output,
        use_gpu=use_gpu,
        overwrite=overwrite,
        video_bitrate=video_bitrate,
        audio_bitrate=audio_bitrate,
        resolution=resolution,
    )
    print(">>>", command)
    try:
        exit_code = system(command, exit_on_errors=False)
    # catch ctrl+c
    except KeyboardInterrupt:
        exit_code = 255

    if exit_code == 255:
        print(f"cleanup (remove {output})...")
        sleep(0.5)
        try:
            os.remove(output)
        except FileNotFoundError:
            pass
        return exit_code


class FFmpeg:
    _gpu: GpuOptions = None

    @classmethod
    def ffmpeg_command(
        cls,
        input: str,
        output: str,
        use_gpu: bool = True,
        overwrite: OverwriteOptions = "ask",
        video_bitrate: str = None,
        audio_bitrate: str = None,
        resolution: [int, int] = None,
    ) -> str:
        """
        generate command for ffmpeg

        :param input: input file path e.g. "input.mov"
        :param output: output file path e.g. "output.mp4"
        :param use_gpu: True=use GPU if exists, False=use CPU
        :param overwrite: "always" "never" "ask"
        :param video_bitrate: e.g. "2M" for 2Mbps
        :param audio_bitrate: e.g. "128K" for 128Kbps
        :param resolution: [width, height] e.g. [-1, 720] for auto:720p
        """
        overwrite_option = cls._get_overwrite_option(overwrite)
        [
            hwaccel_option,
            video_encoder_option,
            hw_extra_filters,
        ] = cls._get_hwaccel_and_encoder_and_extra_filters(use_gpu)
        input_option = cls._get_input_option(input)
        video_bitrate_option = cls._get_bitrate_option("video", video_bitrate)
        audio_bitrate_option = cls._get_bitrate_option("audio", audio_bitrate)
        scale_filter = cls._get_video_filter_scale(resolution)
        video_filter_option = cls._get_video_filter_options(
            [scale_filter, *hw_extra_filters]
        )
        output_option = cls._get_output_option(output)
        return " ".join(
            [
                "ffmpeg",
                overwrite_option,
                hwaccel_option,
                input_option,
                video_bitrate_option,
                audio_bitrate_option,
                video_filter_option,
                video_encoder_option,
                output_option,
            ]
        )

    @classmethod
    def _get_overwrite_option(
        cls,
        overwrite: OverwriteOptions = "ask",
    ) -> str:
        if overwrite == "always":
            return "-y"
        elif overwrite == "never":
            return "-n"
        elif overwrite == "ask":
            return ""
        else:
            raise ValueError(
                f"overwrite param: expected 'always', 'never' or 'ask', got {overwrite}"
            )

    @classmethod
    def detect_gpu(cls) -> GpuOptions:
        if cls._gpu is not None:
            return cls._gpu
        if check_command_exist("nvidia-smi"):
            cls._gpu = "nvidia"
        elif check_command_exist("radeontop"):
            # working on Linux, not working on Windows
            cls._gpu = "amd"
        else:
            print("no GPU detected")
            cls._gpu = "no_gpu"
        return cls._gpu

    @classmethod
    def _get_hwaccel_and_encoder_and_extra_filters(
        cls, use_gpu: bool
    ) -> (str, str, List[str]):
        if not use_gpu:
            return "", "", []
        GPU = cls.detect_gpu()
        if GPU == "nvidia":
            return "-hwaccel cuda", "-c:v hevc_nvenc", []
        elif GPU == "amd" and isWindows:
            return "-hwaccel amf", "-c:v hevc_amf", []
        elif GPU == "amd" and isMacOS:
            raise NotImplementedError
        elif GPU == "amd":
            return "-hwaccel vaapi", "-c:v hevc_vaapi", ["format=nv12", "hwupload"]
        else:
            return "", "hevc", []

    @classmethod
    def _get_input_option(cls, input: str) -> str:
        return f'-i "{input}"'

    @classmethod
    def _get_output_option(cls, output: str) -> str:
        return f'"{output}"'

    @classmethod
    def _get_bitrate_option(cls, type: str, bitrate: str = None) -> str:
        if bitrate is None:
            return ""
        return f"-b:{type[0]} {bitrate}"

    @classmethod
    def _get_video_filter_scale(cls, resolution: [int, int] = None) -> str:
        if resolution is None:
            return ""
        [width, height] = resolution
        return f"scale={width}:{height}"

    @classmethod
    def _get_video_filter_options(cls, filter_list: List[str]) -> str:
        filter_list = list(filter(lambda s: s != "", filter_list))
        if len(filter_list) == 0:
            return ""
        else:
            filter_str = ",".join(filter_list)
            return rf'-vf "{filter_str}"'
