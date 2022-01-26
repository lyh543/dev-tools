#!/bin/bash
pushd ~/git/blog/ >/dev/null

echo
echo pushing to lyh543/blog
echo

git add --all
git commit -m "blog: update on $(date +%c)"
git push origin master

popd  >/dev/null
