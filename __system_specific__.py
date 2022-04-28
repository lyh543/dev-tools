import base64
import os
import sys
import pathlib
import shlex

isWindows = os.name == 'nt'

redirect_stdout_to_null = " >nul" if isWindows else " >/dev/null"
redirect_stderr_to_null = " 2>nul" if isWindows else " 2>/dev/null"


def run_powershell(command: str, load_profile=False) -> int:
    """
    :param command: command
    :param load_profile: if True, load profile for PowerShell
    :return: exit code
    """
    # encode command to escape spaces and other special characters
    encoded_command = base64.b64encode(command.encode(encoding='UTF-16LE')).decode()
    arg_load_profile = '-NoProfile' if not load_profile else ''
    return os.system(f"pwsh.exe {arg_load_profile} -EncodedCommand {encoded_command}")


def run_shell(command: str) -> int:
    return os.system(command)


def system(*commands: str,
           exit_on_errors=True,
           run_pwsh_on_win=False,
           load_profile=False) -> int:
    """
    :param commands: command list, will be joined with &&
    :param exit_on_errors: if True (by default), will exit on errors
    :param run_pwsh_on_win: if True, will run PowerShell on Windows
    :param load_profile: if True, load profile for PowerShell
    :return:
    """
    command = " && ".join(commands)
    exit_code = run_powershell(command, load_profile) if (isWindows and run_pwsh_on_win) else run_shell(command)
    if exit_on_errors and exit_code != 0:
        exit(exit_code)
    return exit_code

