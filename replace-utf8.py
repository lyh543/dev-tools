#!/usr/bin/env python3

from __init__ import *

def replace_utf8(file: str) -> int:
    encodings = ['utf-8', 'gbk', 'gb2312', 'utf-16', 'utf-32']
    encoding = None
    for enc in encodings:
        try:
            with open(file, 'r',newline='\n', encoding=enc) as f:
                content = f.read()
                encoding = enc
                break
        except UnicodeError:
            continue
    if encoding is None:
        print(f'{file} is not encoded in {encodings}')
        return 0
    
    if encoding == 'utf-8':
        print(f'{file} is already utf-8')
    else:
        print(f'{file}: convert {encoding} to utf-8')
        with open(file, 'w',newline='\n', encoding='utf-8') as f:
            f.write(content)

file_extensions = COMMON_FILE_EXTENSIONS
file_patterns = list(map(lambda ext: re.compile(f'\.{ext}$'), file_extensions))
ignored_directory = COMMON_IGNORED_DIRECTORIES

[folder] = argparse("folder", rest="error")
file_list = traverse(folder, file_patterns, ignored_directory)
for file in file_list:
    replace_utf8(file)