import __main__
import pathlib
import sys
from typing import List

from lib.file_filter import *
from lib.system_specific import *

MAIN_FILE = pathlib.Path(__main__.__file__)
PYTHON_EXECUTABLE = sys.executable.replace("\\", "/")


def expand_path(path: str) -> str:
    """
    parse a path with ~ and .
    :param path
    :return: an absolute path
    """
    return str(pathlib.Path(path).expanduser().absolute())


# get "foo.1.2" foo.1.2.txt
def get_stem(file: str) -> str:
    return file[: file.rfind(".")]


def traverse(
    dir_path: str,
    filename_filter: FileFilter = no_filter,
    dirname_filter: FileFilter = no_filter,
) -> List:
    """
    traverse a directory and return a list of files
    will only traverse dirs that dirname_filter(dirname, dirpath) == True
    will only return files that filename_filter(filename, filepath) == True
    """
    total = []
    filenames = os.listdir(dir_path)
    for filename in filenames:
        filepath = os.path.join(dir_path, filename)
        if os.path.isdir(filepath) and dirname_filter(filename, filepath):
            # is a directory and not ignored
            total += traverse(filepath, filename_filter, dirname_filter)
        else:
            if filename_filter(filename, filepath):
                total.append(filepath)
    return total
