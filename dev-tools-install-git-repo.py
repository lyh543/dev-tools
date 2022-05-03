#!/usr/bin/env python3

from __init__ import *

DEV_TOOLS_ROOT = MAIN_FILE.parent
DEV_TOOLS_GIT_HOOKS = DEV_TOOLS_ROOT / '.git' / 'hooks'

POSIX_GIT_PRE_COMMIT = f"""#!/bin/sh
chmod a+x *.py
git update-index --chmod=+x *.py
"""
POSIX_GIT_POST_MERGE = f"""#!/bin/sh
{DEV_TOOLS_ROOT}/dev-tools-install-git-repo.py
{DEV_TOOLS_ROOT}/dev-tools-generate-shell.py
"""
WINDOWS_GIT_PRE_COMMIT = f"""#!/bin/sh
git update-index --chmod=+x *.py
"""
WINDOWS_GIT_POST_MERGE = f"""#!/bin/sh
{DEV_TOOLS_ROOT}/dev-tools-install-git-repo.py
"""

def update_hook(name: str, content: str):
    with open(DEV_TOOLS_GIT_HOOKS / name, 'w', encoding='utf-8') as f:
        f.write(content)
    os.chmod(DEV_TOOLS_GIT_HOOKS / name, 0o755)

update_hook('pre-commit', WINDOWS_GIT_PRE_COMMIT if isWindows else POSIX_GIT_PRE_COMMIT)
update_hook('post-merge', WINDOWS_GIT_POST_MERGE if isWindows else POSIX_GIT_POST_MERGE)
