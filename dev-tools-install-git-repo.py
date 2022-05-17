#!/usr/bin/env python3

from __init__ import *

# todo: add a decorator to log
print('install/update git hooks and other configs...', end='', flush=True)

# config dir
DEV_TOOLS_ROOT = MAIN_FILE.parent
DEV_TOOLS_GIT_HOOKS = DEV_TOOLS_ROOT / '.git' / 'hooks'

DEV_TOOLS_ROOT_POSIX = DEV_TOOLS_ROOT.as_posix()

# commands to be run in the hook
POSIX_GIT_PRE_COMMIT = f"""#!/bin/sh
chmod a+x *.py
git update-index --chmod=+x *.py
echo add execute permission to *.py...done
{DEV_TOOLS_ROOT_POSIX}/dev-tools-install-git-repo.py
"""

POSIX_GIT_POST_MERGE = f"""#!/bin/sh
{DEV_TOOLS_ROOT_POSIX}/dev-tools-install-git-repo.py
"""

WINDOWS_GIT_PRE_COMMIT = f"""#!/bin/sh
git update-index --chmod=+x *.py
echo add execute permission to *.py...done
python {DEV_TOOLS_ROOT_POSIX}/dev-tools-install-git-repo.py
"""

WINDOWS_GIT_POST_MERGE = f"""#!/bin/sh
python {DEV_TOOLS_ROOT_POSIX}/dev-tools-install-git-repo.py
"""


def update_hook(name: str, content: str):
    with open(DEV_TOOLS_GIT_HOOKS / name, 'w', encoding='utf-8') as f:
        f.write(content)
    os.chmod(DEV_TOOLS_GIT_HOOKS / name, 0o755)


update_hook('pre-commit', WINDOWS_GIT_PRE_COMMIT if isWindows else POSIX_GIT_PRE_COMMIT)
update_hook('post-merge', WINDOWS_GIT_POST_MERGE if isWindows else POSIX_GIT_POST_MERGE)

print('done', flush=True)

if not isWindows:
    system(f'python {DEV_TOOLS_ROOT_POSIX}/dev-tools-generate-shell.py')
