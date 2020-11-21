#!/bin/bash
# A sample Bash script, by Ryan
git status
git pull
heroku db:pull
git add .
git commit -m "Deploy"
git push origin main
git push heroku main