#!/bin/bash
# A sample Bash script, by Ryan
git status
git pull
git pull heroku main
git add .
git commit -m "Deploy"
git push origin main
git push heroku main