import base64
import os
import sys
import pathlib
import shlex

isWindows = os.name == 'nt'


def run_powershell(command: str) -> int:
    # encode command to escape spaces and other special characters
    encoded_command = base64.b64encode(command.encode(encoding='UTF-16LE')).decode()
    return os.system(f"pwsh.exe -EncodedCommand {encoded_command}")


def run_shell(command: str) -> int:
    return os.system(command)


def system(*commands: str) -> int:
    command = " && ".join(commands)
    return run_powershell(command) if isWindows else run_shell(command)
