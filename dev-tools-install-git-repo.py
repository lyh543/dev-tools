#!/usr/bin/env python3

from __init__ import *
from lib.log import *

# config dir
DEV_TOOLS_ROOT = MAIN_FILE.parent
DEV_TOOLS_ROOT_POSIX = DEV_TOOLS_ROOT.as_posix()
DEV_TOOLS_GIT_HOOKS = DEV_TOOLS_ROOT / ".git" / "hooks"

# commands to be run in the hook
POSIX_GIT_PRE_COMMIT = f"""#!/bin/sh
set -e
{git_hooks_logging_cmd_started('linting **/*.py')}
black {DEV_TOOLS_ROOT_POSIX}/*.py {DEV_TOOLS_ROOT_POSIX}/**/*.py --check || (black {DEV_TOOLS_ROOT_POSIX}/*.py {DEV_TOOLS_ROOT_POSIX}/**/*.py; exit 1)
{git_hooks_logging_cmd_done('linting **/*.py')}
python3 {DEV_TOOLS_ROOT_POSIX}/dev-tools-install-git-repo.py
"""

WINDOWS_GIT_PRE_COMMIT = f"""#!/bin/sh
set -e
{git_hooks_logging_cmd_started('linting **/*.py')}
black {DEV_TOOLS_ROOT_POSIX}/*.py {DEV_TOOLS_ROOT_POSIX}/**/*.py --check || (black {DEV_TOOLS_ROOT_POSIX}/*.py {DEV_TOOLS_ROOT_POSIX}/**/*.py; exit 1)
{git_hooks_logging_cmd_done('linting **/*.py')}

{PYTHON_EXECUTABLE} {DEV_TOOLS_ROOT_POSIX}/dev-tools-install-git-repo.py
"""

POSIX_GIT_POST_MERGE = f"""#!/bin/sh
python3 {DEV_TOOLS_ROOT_POSIX}/dev-tools-install-git-repo.py
"""

WINDOWS_GIT_POST_MERGE = f"""#!/bin/sh
{PYTHON_EXECUTABLE} {DEV_TOOLS_ROOT_POSIX}/dev-tools-install-git-repo.py
"""


@git_hooks_logging("install/update git hooks")
def update_git_hooks():
    def update_hook(name: str, content: str):
        with open(DEV_TOOLS_GIT_HOOKS / name, "w", encoding="utf-8") as f:
            f.write(content)
        os.chmod(DEV_TOOLS_GIT_HOOKS / name, 0o755)

    update_hook(
        "pre-commit", WINDOWS_GIT_PRE_COMMIT if isWindows else POSIX_GIT_PRE_COMMIT
    )
    update_hook(
        "post-merge", WINDOWS_GIT_POST_MERGE if isWindows else POSIX_GIT_POST_MERGE
    )


if __name__ == "__main__":
    update_git_hooks()
    system(f"{PYTHON_EXECUTABLE} {DEV_TOOLS_ROOT_POSIX}/dev-tools-generate-shell.py")
