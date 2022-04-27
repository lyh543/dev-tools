from __system_specific__ import *
import __main__
import pathlib
from typing import Literal


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
        filename = pathlib.Path(__main__.__file__).name
        wrapped_argnames = shlex.join(map(lambda x: '<' + x + '>', argnames))
        print(f'Usage: {filename} {wrapped_argnames}')
        sys.exit(1)

    exact_params = args[:len(argnames)]
    rest_params = args[len(argnames):]
    if rest == 'return':
        return exact_params + [' '.join(rest_params)]
    else:
        return exact_params
