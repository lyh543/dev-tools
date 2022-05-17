import re

from lib.system_specific import *
import __main__
import pathlib
from typing import Literal, Callable

MAIN_FILE = pathlib.Path(__main__.__file__)
TEXT_FILE_EXTENSIONS = ['py', 'html', 'css', 'js', 'json', 'md', 'ts', 'tsx', 'txt', 'bat', 'sh', 'ps1']
VIDEO_FILE_EXTENSIONS = ['mp4', 'avi', 'mkv', 'mov', 'm4v', 'webm', 'wmv', 'flv', 'vob', 'ogv', 'ogg' 'mpg', 'mpeg',
                         'm2v', 'm4p', 'm4v', 'mp4v', 'svi', '3gp', '3g2', 'mxf', 'roq', 'nsv', 'f4v', 'f4p', 'f4a',
                         'f4b']
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
             file_patterns: Callable[[str], bool] = lambda x: True,
             ignored_directories: Callable[[str], bool] = lambda x: True) -> list:
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
