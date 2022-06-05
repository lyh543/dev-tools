#!/usr/bin/env python3

from __init__ import *
from datetime import datetime

print("\npushing to lyh543/blog\n")

system(
    "pushd ~/git/blog/" + REDIRECT_STDOUT_TO_NULL,
    "git add --all",
    f"git commit -m 'blog: update on {datetime.now()}'",
    "git push origin master",
    "popd" + REDIRECT_STDOUT_TO_NULL,
    run_pwsh_on_win=True,
)
