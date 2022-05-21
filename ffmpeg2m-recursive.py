#!/usr/bin/env python3

from __init__ import *
from ffmpeg2m import ffmpeg2m


def ffmpeg2m_recursive(path="."):
    """
    :param path: directory path
    :return: if is exited by Ctrl+C, clean unfinished output and return 255
    """
    file_list = traverse(path,
                         filename_filter=extension_allow_filter(VIDEO_FILE_EXTENSIONS),
                         dirname_filter=filename_block_filter(COMMON_IGNORED_DIRECTORIES))
    filtered_file_list = list(filter(lambda f: f.split('.')[-2] != 'compressed' and
                                               f.split('.')[:-1] + '.compressed.mp4' not in file_list,
                                     file_list))
    output_list = list(map(lambda f: '.'.join(f.split('.')[:-1]) + '.compressed.mp4', filtered_file_list))

    input_output_list = list(zip(filtered_file_list, output_list))
    input_output_str = map(lambda x: ' -> '.join(x), input_output_list)
    print("file_list:", "\n".join(input_output_str), sep='\n', end='\n\n')
    for i in range(len(input_output_list)):
        [input, output] = input_output_list[i]
        print(f'[{i + 1}/{len(input_output_list)}] ', end='')
        value = ffmpeg2m(input, output, overwrite=False)
        if value == 255:
            exit(value)
        print('\n')


if __name__ == '__main__':
    [path] = argparse(rest='return')
    if path == "":
        path = "."
    ffmpeg2m_recursive(path)
