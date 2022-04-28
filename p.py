#!/usr/bin/env python3

from __init__ import *
from datetime import datetime

print("\npushing to lyh543/blog\n")

system(
    "pushd ~/git/blog/" + redirect_stdout_to_null,
    "git add --all",
    f"git commit -m 'blog: update on {datetime.now()}'",
    "git push origin master",
    "popd" + redirect_stdout_to_null,
    run_pwsh_on_win=True,
)
