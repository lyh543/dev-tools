from .system_specific import *


def image_resize(input: str, output: str, resolution: [int, int]):
    """
    run `convert` to resize an image

    :param input: input file path e.g. "input.jpg"
    :param output: output file path e.g. "output.jpg"
    :param resolution: [width, height] e.g. [-1, 720] for auto:720p
    :return:
    """
    resolution_str = "x".join(map(lambda v: str(v) if v > 0 else "", resolution))
    resolution_option = f"-resize {resolution_str}"
    return system(f'convert "{input}" {resolution_option} "{output}"')


def image_compress(input: str, size: int):
    """
    run `jpegoptim` to compress an image to specific size

    :param input: input file path e.g. "input.jpg". output will overwrite input.
    :param size: output_size in KB
    :return:
    """
    return system(f'jpegoptim --size={size} "{input}"')
