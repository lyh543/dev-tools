#!/usr/bin/env python3

from __init__ import *
from ffmpeg2m import ffmpeg2m


def ffmpeg2m_recursive(path = "."):
    """
    :param path: directory path
    :return: if is exited by Ctrl+C, clean unfinished output and return 255
    """
    file_list = traverse(path, VIDEO_FILE_EXTENSIONS, COMMON_IGNORED_DIRECTORIES)
    filtered_file_list = list(filter(lambda f: f.split('.')[-2] != 'compressed', file_list))
    output_list = list(map(lambda f: '.'.join(f.split('.')[:-1]) + '.compressed.mp4', filtered_file_list))

    input_output_list = list(zip(filtered_file_list, output_list))
    input_output_str = map(lambda x: ' -> '.join(x), input_output_list)
    print("file_list:", "\n".join(input_output_str),  sep='\n', end='\n\n')
    for input, output in input_output_list:
        value = ffmpeg2m(input, output, overwrite=False)
        if value == 255:
            exit(value)


if __name__ == '__main__':
    [path] = argparse(rest='return')
    if path == "":
        path = "."
    ffmpeg2m_recursive(path)
