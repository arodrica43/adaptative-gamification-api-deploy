#!/bin/bash
# A sample Bash script, by Ryan
to=~/Documentos/feina/dev/deploy/gamification-app/
cp -r adaptative_gamification $to
cp db.sqlite3 $to
cp LICENSE $to
cp -r media $to
cp requirements.txt $to
cp -r api $to
cp favicon.ico $to
cp manage.py $to
cp README.md $to
cp -r static $to
cp -r .gitignore $to
cp -r Procfile $to
cd ~/Documentos/feina/dev/deploy/gamification-app/
echo "+ Gamification-App local dir updated"
git status
git pull
git add .
git commit -m "Automatic Production Deploy"
git push origin master
echo "+ Gamification-App GitLab updated"