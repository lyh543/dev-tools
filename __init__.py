import re
from typing import Literal

from lib.system_specific import *
from lib.file_filter import *
import __main__
import pathlib

MAIN_FILE = pathlib.Path(__main__.__file__)


def expand_path(path: str) -> str:
    """
    parse a path with ~ and .
    :param path
    :return: an absolute path
    """
    return str(pathlib.Path(path).expanduser().absolute())


def argparse(
    *argnames: str, rest: Literal["error", "ignore", "return"] = "ignore"
) -> list[str]:
    """
    Usage:
        [param1, param2] = argparse("param1", "param2")
        [param1, param2, rest] = argparse("param1", "param2", rest='return')
    """
    args = sys.argv[1:]
    if len(args) < len(argnames) or (len(args) > len(argnames) and rest == "error"):
        filename = MAIN_FILE.name
        wrapped_argnames = " ".join(map(lambda x: "<" + x + ">", argnames))
        print(f"Usage: {filename} {wrapped_argnames}")
        sys.exit(1)

    exact_params = args[: len(argnames)]
    rest_params = args[len(argnames) :]
    if rest == "return":
        return exact_params + [shlex.join(rest_params)]
    else:
        return exact_params


def traverse(
    dir_path: str,
    filename_filter: FileFilter = no_filter,
    dirname_filter: FileFilter = no_filter,
) -> list:
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
