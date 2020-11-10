# Adaptative Gamification Module

An Django Web App (+ API!) to embed adaptative gamification mechanics (as well as common mechanics) in your web project. All data involved with the mechanics is managed through this application, so content developers needn't care about managing gamification data, while they offer a gamified experience. This is a project from Barcelona University, namely NanoMOOC UB project, so for any use of it, contact with nanomoocsub@gmail.com

## Features ##

Currently, the web-app have 2 main features:

1) Incrustable code generation for the following gamification mechanics: (+ API!) 

	- Development Tools (Disruptor)
	- Challenges (Disruptor)
	- Easter Eggs (Free spirit)
	- Unlockables (Free spirit)
	- Badges (Achiever)
	- Levels (Achiever)
	- Points (Player)
	- Leaderboards (Player)
	- Lotteries (Player)
	- Gift Openers (Player)
	- Social Networks (Socializer)
	- Social Statuses (Socializer)
	- Sharing Knowledge (Philantropist)
	- Gifts (Philantropist)

2) Gamified user data management (create, read, write and delete) structured as: (+ API!) 

	- Personal Profile (Username, e-mail, ...)
	- Gamer Profile (Badges, Challenges, Score, ...)
	- Emotional Profile (In dependence with Emotion Detection Module)
	- Social Profile (Friends, Followers, Views, Avatar, ...)

## Install and Run (Local) ##

This is a Django Application, so just install the python libraries from requirements.txt.
To run locally the django project at port 8080 use 

```
python manage.py runserver 8080
```

## Deploy on a AWS instance ##

I haven't tried this option yet, but the link below could help:

https://aws.amazon.com/es/getting-started/hands-on/deploy-python-application/

## Usage ##

To use the embedding code of a mechanic, follow the steps:

1) Go to /g_mechanics/list
2) Preview the mechanic you want to embed
3) Click on "Get Incrustable Code" button
4) Copy the code inside the square
5) Paste that code inside the body of an HTML template.

The API must be used through the HTTPS protocol.

## Example ## 

You can find a deployed version of the AGModule at https://agmodule.herokuapp.com



