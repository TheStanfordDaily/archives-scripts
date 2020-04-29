#!/bin/bash
cd ../archives-text/
echo "Currently in:"
pwd
echo "Adding all files"
git add -A
echo "Added all files. Now committing"
git commit -m "archives-text-git.sh: fixed"
echo "Committed, now checkout new branch"
git checkout -b fix-repeats
echo "Checkedout new branch, pushing now"
git push origin fix-repeats
echo "Done"
