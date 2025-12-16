def get_compressed_output_path(input_path: str) -> str:
    """
    Generate the output path for the compressed video file.
    :param input_path: The path of the input video file.
    :return: The path for the compressed video file.
    """
    return input_path[: input_path.rfind(".")] + ".compressed.mp4"
