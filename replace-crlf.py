#!/usr/bin/env python3

from __init__ import *


def replace_pattern(file: str, old: str, new: str) -> int:
    """
    replace patterns in a file
    :param file: file path
    :param old: old string
    :param new: new string
    :return: if any pattern is replaced, return 1, otherwise return 0
    """
    encodings = ['utf-8', 'gbk', 'gb2312', 'utf-16', 'utf-32']
    encoding = None
    for enc in encodings:
        try:
            with open(file, 'r', newline='\n', encoding=enc) as f:
                content = f.read()
                encoding = enc
                break
        except UnicodeError:
            continue
    if encoding is None:
        print(f'{file} is not encoded in {encodings}')
        return 0

    if old in content:
        content = content.replace(old, new)
        with open(file, 'w', newline='\n', encoding=encoding) as f:
            f.write(content)
            print('replace pattern in ' + file)
        return 1
    else:
        return 0


[folder] = argparse("folder", rest="error")
file_list = traverse(folder,
                     filename_filter=extension_allow_filter(TEXT_FILE_EXTENSIONS),
                     dirname_filter=filename_block_filter(COMMON_IGNORED_DIRECTORIES))
for file in file_list:
    replace_pattern(file, '\r\n', '\n')
