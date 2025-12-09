from functools import lru_cache
import logging
from time import sleep
from typing import List, Literal, Optional, Tuple

from .system_specific import *

OverwriteOptions = Literal["always", "never", "ask"]
GpuOptions = Literal["nvidia", "amd", "amd_apu", "no_gpu", None]


def ffmpeg(
    input: str,
    output: str,
    use_gpu: bool = True,
    overwrite: OverwriteOptions = "ask",
    video_bitrate: str = None,
    audio_bitrate: str = None,
    resolution: Tuple[int, int] = None,
    fps: Optional[int] = None,
    fps_change_mode: Literal["output", "vsync"] = "vsync",
    drop_duplicate_frames: bool = False,
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
    :param fps: e.g. 30 for 30fps
    :param: fps_change_mode: "vsync" for "-vf 'fps=xxx' -vsync 2", or "output" for "-r xxx" option. See https://trac.ffmpeg.org/wiki/ChangingFrameRate'
    :param drop_duplicate_frames: whether use mpdecimate filter to drop duplicate frames
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
            fps=fps,
            fps_change_mode=fps_change_mode,
            drop_duplicate_frames=drop_duplicate_frames,
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
        fps: Optional[int] = None,
        fps_change_mode: Literal["output", "vsync"] = "vsync",
        drop_duplicate_frames: bool = False,
        resolution: Optional[Tuple[int, int]] = None,
    ) -> str:
        """
        generate command for ffmpeg

        :param input: input file path e.g. "input.mov"
        :param output: output file path e.g. "output.mp4"
        :param use_gpu: True=use GPU if exists, False=use CPU
        :param overwrite: "always" "never" "ask"
        :param video_bitrate: e.g. "2M" for 2Mbps
        :param audio_bitrate: e.g. "128K" for 128Kbps
        :param fps: e.g. 30 for 30fps.
        :param fps_change_mode: "vsync" for "-vf 'fps=xxx' -vsync 2", or "output" for "-r xxx" option. See https://trac.ffmpeg.org/wiki/ChangingFrameRate
        :param drop_duplicate_frames: whether use mpdecimate filter to drop duplicate frames
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
        if fps_change_mode == "vsync":
            fps_option = ""
            fps_filter = cls._get_video_filter_fps(fps)
            vsync_option = cls._get_vsync_option(2)
        else:
            fps_option = cls._get_fps_option(fps)
            fps_filter = ""
            vsync_option = ""
        mpdecimate_filter = cls._get_video_filter_mpdecimate(
            drop_duplicate_frames, use_gpu=use_gpu
        )
        scale_filter = cls._get_video_filter_scale(resolution, use_gpu=use_gpu)
        video_filter_option = cls._get_video_filter_options(
            [fps_filter, mpdecimate_filter, scale_filter, *hw_extra_filters]
        )
        output_option = cls._get_output_option(output)
        return " ".join(
            [
                "ffmpeg",
                "-hide_banner",
                overwrite_option,
                hwaccel_option,
                input_option,
                video_bitrate_option,
                audio_bitrate_option,
                video_filter_option,
                video_encoder_option,
                vsync_option,
                fps_option,
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
                "-hide_banner",
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
                "-hide_banner",
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
        # Prefer NVIDIA if present
        if check_command_exist("nvidia-smi"):
            cls._gpu = "nvidia"
            return cls._gpu
        # Windows: detect AMD via vendor ID or compatibility string
        if isWindows:
            ps = "If (Get-CimInstance Win32_VideoController | Where-Object {$_.PNPDeviceID -match 'VEN_1002' -or $_.AdapterCompatibility -match 'Advanced Micro Devices'}) { exit 0 } else { exit 1 }"
            exit_code = run_powershell(ps)
            if exit_code == 0:
                cls._gpu = "amd"
                return cls._gpu
        # Linux/Unix: detect VAAPI/APU (cannot distinguish discrete vs APU reliably here)
        if check_command_exist("vainfo"):
            cls._gpu = "amd_apu"  # TODO: distinguish AMD GPU and APU
            return cls._gpu
        # elif check_command_exist("radeontop"):
        #     # working on Linux, not working on Windows
        #     cls._gpu = "amd"
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
        """
        get hardware acceleration option, encoder option and extra filters for ffmpeg command.

        Returns:
            Tuple[str, str, List[str]]: hwaccel option, encoder option, extra filters
        """
        if not use_gpu:
            return "", cls._get_encoder_option("hevc"), []
        GPU = cls.detect_gpu()
        logging.info(f"detect GPU: {GPU}")
        if GPU == "nvidia":
            return "-hwaccel cuda", cls._get_encoder_option("hevc_nvenc"), []
        elif GPU == "amd_apu":
            return (
                "-hwaccel vaapi -hwaccel_output_format vaapi",
                cls._get_encoder_option("hevc_vaapi"),
                ["hwupload"],
            )
        elif GPU == "amd" and isWindows:
            # decode via Direct3D 11, encode via AMF
            return "-hwaccel d3d11va", cls._get_encoder_option("hevc_amf"), []
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
        return f"-b:{type[0]} {bitrate}" if bitrate else ""

    @classmethod
    def _get_fps_option(cls, fps: Optional[int] = None) -> str:
        return f"-r {fps}" if fps else ""

    @classmethod
    def _get_vsync_option(cls, vsync: Optional[int] = None) -> str:
        return f"-vsync {vsync}" if vsync else ""

    @classmethod
    def _get_video_filter_scale(
        cls, resolution: Optional[Tuple[int, int]], use_gpu: bool
    ) -> str:
        if resolution is None:
            return ""
        [width, height] = resolution
        if use_gpu and cls._gpu == "amd_apu":
            # AMD APU requires vaapi filter for scaling
            return f"scale_vaapi=w={width}:h={height}:format=nv12"
        return f"scale={width}:{height}"

    @classmethod
    def _get_video_filter_fps(cls, fps: Optional[int] = None) -> str:
        return f"fps={fps}" if fps else ""

    @classmethod
    def _get_video_filter_mpdecimate(cls, mpdecimate: bool, use_gpu: bool) -> str:
        # AMD APU does not support mpdecimate filter
        if use_gpu and cls._gpu == "amd_apu":
            return ""
        return "mpdecimate" if mpdecimate else ""

    @classmethod
    def _get_video_filter_options(cls, filter_list: List[str]) -> str:
        filter_list = list(filter(lambda s: s != "", filter_list))
        if len(filter_list) == 0:
            return ""
        else:
            filter_str = ",".join(filter_list)
            return rf'-vf "{filter_str}"'
