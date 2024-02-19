import logging
from time import sleep
from typing import List, Literal, Optional, Tuple

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
    resolution: Tuple[int, int] = None,
    rate: int = None,
    prepend_video_filters: List[str] = None,
    copy_mode: bool = False,
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
    :param rate: e.g. 30 for 30fps
    :param prepend_video_filters: e.g. ["mpdecimate"]
    :param copy_mode: True=copy video and audio stream, False=encode video and audio stream
    """
    if copy_mode:
        command = FFmpeg.ffmpeg_copy_command(
            input=input,
            output=output,
            overwrite=overwrite,
        )
    elif not output.endswith("mp3"):
        command = FFmpeg.ffmpeg_command(
            input=input,
            output=output,
            use_gpu=use_gpu,
            overwrite=overwrite,
            video_bitrate=video_bitrate,
            audio_bitrate=audio_bitrate,
            resolution=resolution,
            rate=rate,
            prepend_video_filters=prepend_video_filters,
        )
    else:
        command = FFmpeg.ffmpeg_audio_command(
            input=input,
            output=output,
            overwrite=overwrite,
            audio_bitrate=audio_bitrate,
        )
    print(">>>", command)
    try:
        exit_code = system(command, exit_on_errors=False)
    # catch ctrl+c
    except KeyboardInterrupt:
        exit_code = 255
    if exit_code > 0:
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
        video_bitrate: Optional[str] = None,
        audio_bitrate: Optional[str] = None,
        rate: Optional[int] = None,
        resolution: Optional[Tuple[int, int]] = None,
        prepend_video_filters: Optional[List[str]] = None,
    ) -> str:
        """
        generate command for ffmpeg

        :param input: input file path e.g. "input.mov"
        :param output: output file path e.g. "output.mp4"
        :param use_gpu: True=use GPU if exists, False=use CPU
        :param overwrite: "always" "never" "ask"
        :param video_bitrate: e.g. "2M" for 2Mbps
        :param audio_bitrate: e.g. "128K" for 128Kbps
        :param rate: e.g. 30 for 30fps
        :param resolution: [width, height] e.g. [-1, 720] for auto:720p
        :param prepend_video_filters: e.g. ["mpdecimate"]
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
        rate_option = cls._get_rate_option(rate)
        scale_filter = cls._get_video_filter_scale(resolution)
        video_filter_option = cls._get_video_filter_options(
            [*(prepend_video_filters or []), scale_filter, *hw_extra_filters]
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
                rate_option,
                video_filter_option,
                video_encoder_option,
                output_option,
            ]
        )

    @classmethod
    def ffmpeg_audio_command(
        cls,
        input: str,
        output: str,
        overwrite: OverwriteOptions = "ask",
        audio_bitrate: str = None,
    ) -> str:
        """
        generate command for ffmpeg

        :param input: input file path e.g. "input.mov"
        :param output: output file path e.g. "output.mp4"
        :param overwrite: "always" "never" "ask"
        :param audio_bitrate: e.g. "128K" for 128Kbps
        """
        overwrite_option = cls._get_overwrite_option(overwrite)
        input_option = cls._get_input_option(input)
        audio_bitrate_option = cls._get_bitrate_option("audio", audio_bitrate)
        output_option = cls._get_output_option(output)
        return " ".join(
            [
                "ffmpeg",
                overwrite_option,
                input_option,
                audio_bitrate_option,
                output_option,
            ]
        )

    @classmethod
    def ffmpeg_copy_command(
        cls,
        input: str,
        output: str,
        overwrite: OverwriteOptions = "ask",
        video_encoder="copy",
        audio_encoder="copy",
    ) -> str:
        """
        generate command for ffmpeg

        :param input: input file path e.g. "input.mov"
        :param output: output file path e.g. "output.mp4"
        :param overwrite: "always" "never" "ask"
        :param video_encode: e.g. "copy" or "hevc"
        :param audio_encode: e.g. "copy" or "aac"
        """
        overwrite_option = cls._get_overwrite_option(overwrite)
        input_option = cls._get_input_option(input)
        video_encoder_option = cls._get_encoder_option(video_encoder, audio_encoder)
        output_option = cls._get_output_option(output)
        return " ".join(
            [
                "ffmpeg",
                overwrite_option,
                input_option,
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
        # elif check_command_exist("radeontop"):
        #     # working on Linux, not working on Windows
        #     cls._gpu = "amd"
        else:
            print("no GPU detected")
            cls._gpu = "no_gpu"
        return cls._gpu

    @classmethod
    def _get_encoder_option(cls, video_encoder: str, audio_encoder="aac") -> str:
        return f"-c:v {video_encoder} -c:a {audio_encoder}"

    @classmethod
    def _get_hwaccel_and_encoder_and_extra_filters(
        cls, use_gpu: bool
    ) -> Tuple[str, str, List[str]]:
        if not use_gpu:
            return "", cls._get_encoder_option("hevc"), []
        GPU = cls.detect_gpu()
        logging.info(f"detect GPU: {GPU}")
        if GPU == "nvidia":
            return "-hwaccel cuda", cls._get_encoder_option("hevc_nvenc"), []
        elif GPU == "amd" and isWindows:
            return "-hwaccel amf", cls._get_encoder_option("hevc_amf"), []
        elif GPU == "amd" and isMacOS:
            raise NotImplementedError
        elif GPU == "amd":
            return (
                "-hwaccel vaapi",
                cls._get_encoder_option("hevc_vaapi"),
                ["format=nv12", "hwupload"],
            )
        else:
            return "", cls._get_encoder_option("hevc"), []

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
    def _get_rate_option(cls, rate: int = None) -> str:
        if rate is None:
            return ""
        return f"-r {rate}"

    @classmethod
    def _get_video_filter_scale(cls, resolution: Tuple[int, int] = None) -> str:
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
