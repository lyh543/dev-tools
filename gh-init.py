#!/usr/bin/env python3

from __init__ import *

system(
    'git config --global user.email                      "lyh543@outlook.com"',
    'git config --global user.name                       "lyh543"',
    'git config --global includeif.gitdir:bitme/.path    ".bitme.gitconfig"',
    'git config --global pull.rebase                     "true"',
    'git config --global diff.submodule                  "log"',
    'git config --global init.defaultbranch              "master"',
    'git config --global http.proxy                      "http://127.0.0.1:17296"',
    'git config --global https.proxy                     "http://127.0.0.1:17296"',

    'git config --global core.editor                     "code --wait"',
    'git config --global core.autocrlf                   "input"',

    'git config --file $HOME/.bitme.gitconfig user.email       "yan.lyh@bitme.fun"',
    'git config --file $HOME/.bitme.gitconfig user.name        "Yanhui Liu"',
    run_pwsh_on_win=True,
)
