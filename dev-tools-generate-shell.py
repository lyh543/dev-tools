#!/usr/bin/env python3

import shutil
from __init__ import *
from lib.log import git_hooks_logging

DEV_TOOLS_ROOT = MAIN_FILE.parent
TARGET_DIR = DEV_TOOLS_ROOT / "shell"


def generate_shell_windows(basename: str):
    if (
        system(
            "where.exe " + basename + redirect_stdout_to_null + redirect_stderr_to_null,
            exit_on_errors=False,
        )
        == 0
    ):
        print(basename + " command already exists, skip")
        return
    with open(TARGET_DIR / (basename + ".cmd"), "w", encoding="utf-8") as f:
        f.write(r"@python.exe %~dp0\..\%~n0.py %*")


def generate_shell_linux(basename: str):
    if (
        system(
            "which " + basename + redirect_stdout_to_null + redirect_stderr_to_null,
            exit_on_errors=False,
        )
        == 0
    ):
        print(basename + " command already exists, skip")
        return
    with open(TARGET_DIR / basename, "w", encoding="utf-8") as f:
        f.write(
            f"""#!/bin/sh \n""" + f"""python {DEV_TOOLS_ROOT}/{basename}.py "$@" """
        )
    os.chmod(TARGET_DIR / basename, 0o755)


@git_hooks_logging("generate shell shortcuts for linux")
def generate_shell():
    shutil.rmtree(TARGET_DIR, ignore_errors=True)
    os.makedirs(TARGET_DIR)

    for file in os.listdir(DEV_TOOLS_ROOT):
        if not re.match("^.*\\.py$", file) or re.match("^[_.].*$", file):
            continue
        basename = file[0:-3]

        if isWindows:
            generate_shell_windows(basename)
        else:
            generate_shell_linux(basename)

    if str(TARGET_DIR) not in os.environ["PATH"]:
        print(
            "Detected missing in PATH. Remember to add the following command to .bashrc or .zshrc :"
        )
        print(f'export PATH="$PATH:{TARGET_DIR}"')


if __name__ == "__main__":
    generate_shell()
