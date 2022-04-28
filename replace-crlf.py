#!/usr/bin/env python3

from __init__ import *


file_extensions = COMMON_FILE_EXTENSIONS
file_patterns = list(map(lambda ext: re.compile(f'\.{ext}$'), file_extensions))
ignored_directory = COMMON_IGNORED_DIRECTORIES

[folder] = argparse("folder", rest="error")
file_list = traverse(folder, file_patterns, ignored_directory)
for file in file_list:
    replace_pattern(file, '\r\n', '\n')