![travis ci](https://travis-ci.org/arodrica43/adaptative-gamification-api-deploy.svg?branch=main)

# Gamification Module App

#### Gamification Module - Web App ####

## Table of contents
* [General info](#general-info)
* [Features](#features)
* [Install and Run (Local)](#install-and-run)
* [Deploy](#deploy)
* [Usage](#usage)
* [Demo](#demo)

## General info

A Django Web App (+ API!) to embed adaptative gamification mechanics (as well as common mechanics) in your web project. All data involved with the mechanics is managed through this application, so content developers needn't care about managing gamification data, while they offer a gamified experience. This is a project from Barcelona University, namely NanoMOOC UB project, so for any use of it, contact with nanomoocsub@gmail.com

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

This is a Django Application, so just install the python dependences from requirements.txt. This app is developed with Python-3.7.3.
To run locally the django project at port 8080 use 

```
python manage.py runserver 8080
```

## Deploy ##

When this Django app is deployed, the default database (db.sqlite3) should be recreated. Its creation depends on the deploying platform, but basically, you should follow this steps:

1) Create a database (tested with sqlite and postgresql).
2) (Optional) Create database migrations with

```
python manage.py makemigrations
```

2) Migrate the database:

```
python manage.py migrate
```

3) Create an administrator user:

```
python manage.py createsuperuser
```

4) Add the domain url into ALOWED_HOSTS, in adaptative_gamification/settings.py
5) Find and replace all project occurrences of the form "agmodule.herokuapp.com" by the domain url where the project is being deployed. 


### Deploy on AWS ###

I haven't tried this option yet, but the link below could help:

https://aws.amazon.com/es/getting-started/hands-on/deploy-python-application/

## Usage ##

To use the embedding code of a mechanic, follow the steps:

1) Go to api/g_mechanics/
2) Preview the mechanic you want to embed 
``` 
api/g_mechanics/<id>/preview?<required_arguments> 

```
3) Click on "Get Incrustable Code" button
4) Copy the code inside the square
5) Paste that code inside the body of a HTML template.

The API must be used with the HTTPS protocol.

## Demo ## 

You can find a deployed version of the AGModule at https://agmodule.herokuapp.com

