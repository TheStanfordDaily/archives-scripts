#!/bin/bash
cd ../archives-text/
ls
git checkout -b "fix-repeats"
git add *
git commit -m "archives-text-git.sh: fixed"
git push origin fix-repeats
