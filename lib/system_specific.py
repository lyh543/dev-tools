import base64
import os

isWindows = os.name == "nt"
isMacOS = os.name == "posix" and os.uname()[0] == "Darwin"

# redirect stdout and stderr to null on both Windows and Unix
# Usage 1: append to specific command to avoid printing
# Usage 2: use system(redirect_stdout_to_null=True) to avoid printing in all commands
REDIRECT_STDOUT_TO_NULL = " >nul" if isWindows else " >/dev/null"
REDIRECT_STDERR_TO_NULL = " 2>nul" if isWindows else " 2>/dev/null"


def run_powershell(command: str, load_profile=False) -> int:
    """
    :param command: command
    :param load_profile: if True, load profile for PowerShell
    :return: exit code
    """
    # encode command to escape spaces and other special characters
    encoded_command = base64.b64encode(command.encode(encoding="UTF-16LE")).decode()
    arg_load_profile = "-NoProfile" if not load_profile else ""
    return os.system(f"pwsh.exe {arg_load_profile} -EncodedCommand {encoded_command}")


def run_shell(command: str) -> int:
    return os.system(command)


def system(
    *commands: str,
    redirect_stdout_to_null=False,
    redirect_stderr_to_null=False,
    exit_on_errors=True,
    run_pwsh_on_win=False,
    load_profile=False,
) -> int:
    """
    run command

    :param commands: command list, will be joined with &&
    :param redirect_stdout_to_null: if True, redirect all stdout to null
    :param redirect_stderr_to_null: if True, redirect all stderr to null
    :param exit_on_errors: if True (by default), will exit on errors
    :param run_pwsh_on_win: if True, will run PowerShell on Windows
    :param load_profile: if True, load profile for PowerShell
    :return: exit code
    """
    if redirect_stdout_to_null:
        commands = map(lambda x: x + REDIRECT_STDOUT_TO_NULL, commands)
    if redirect_stderr_to_null:
        commands = map(lambda x: x + REDIRECT_STDERR_TO_NULL, commands)
    joined_command = " && ".join(commands)
    exit_code = (
        run_powershell(joined_command, load_profile)
        if (isWindows and run_pwsh_on_win)
        else run_shell(joined_command)
    )
    if exit_on_errors and exit_code != 0:
        exit(exit_code)
    return exit_code


def start_shell() -> int:
    """
    start a shell, usually after changing directory in Python

    :return: exit code
    """
    return os.system("pwsh || powershell || cmd") if isWindows else os.system("$SHELL")


def check_command_exist(command: str) -> bool:
    """
    check if command exists

    :param command: command
    :return: True if command exists
    """
    if isWindows:
        which = "where.exe " + command
    else:
        which = "which " + command
    return (
        system(
            which,
            redirect_stdout_to_null=True,
            redirect_stderr_to_null=True,
            exit_on_errors=False,
        )
        == 0
    )
