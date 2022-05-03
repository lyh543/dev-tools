import re

from lib.system_specific import *
import __main__
import pathlib
from typing import Literal

MAIN_FILE = pathlib.Path(__main__.__file__)
COMMON_FILE_EXTENSIONS = ['py', 'html', 'css', 'js', 'json', 'md', 'ts', 'tsx', 'txt', 'bat', 'sh', 'ps1']
COMMON_IGNORED_DIRECTORIES = ['node_modules', '.git', '.idea', '.vscode', 'build', 'dist', '__pycache__']


def expand_path(path: str) -> str:
    """
    parse a path with ~ and .
    :param path
    :return: an absolute path
    """
    return str(pathlib.Path(path).expanduser().absolute())


def argparse(*argnames: str, rest: Literal['error', 'ignore', 'return'] = 'ignore') -> list[str]:
    """
    Usage:
        [param1, param2] = argparse("param1", "param2")
        [param1, param2, rest] = argparse("param1", "param2", rest='return')
    """
    args = sys.argv[1:]
    if len(args) < len(argnames) or (len(args) > len(argnames) and rest == 'error'):
        filename = MAIN_FILE.name
        wrapped_argnames = ' '.join(map(lambda x: '<' + x + '>', argnames))
        print(f'Usage: {filename} {wrapped_argnames}')
        sys.exit(1)

    exact_params = args[:len(argnames)]
    rest_params = args[len(argnames):]
    if rest == 'return':
        return exact_params + [shlex.join(rest_params)]
    else:
        return exact_params


def traverse(dir_path: str,
             file_patterns: list[str | re.Pattern] = None,
             ignored_directories: list[str | re.Pattern] = None) -> list:
    """
    traverse a directory and return a list of files (folders are excluded)
    """
    if file_patterns is None:
        file_patterns = []
    if ignored_directories is None:
        ignored_directories = []
    total = []
    filenames = os.listdir(dir_path)
    for filename in filenames:
        full_path = os.path.join(dir_path, filename)
        if os.path.isdir(full_path):
            # is a directory and not ignored
            if not any(map(lambda x: re.search(x, filename), ignored_directories)):
                total += traverse(full_path, file_patterns, ignored_directories)
        else:
            # is a file and matched the pattern
            if any(map(lambda x: re.search(x, filename), file_patterns)):
                total.append(full_path)
    return total


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
            with open(file, 'r',newline='\n', encoding=enc) as f:
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
        with open(file, 'w',newline='\n', encoding=encoding) as f:
            f.write(content)
            print('replace pattern in ' + file)
        return 1
    else:
        return 0