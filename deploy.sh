#!/bin/bash
# A sample Bash script, by Ryan
git status
git pull
git add .
git commit -m "Deploy"
git push origin main
echo "+ Gamification-App Git updated"
git push heroku main
echo "+ Gamification-App Heroku app updated"