# MTA Tracker

## Introduction
MTA Tracker is a small web service to monitor NYC MTA subway service. The web service provides two endpoints ```/status``` and ```/uptime```
that can be used to check delays and uptime for a given subway line.

## Given Requirements
* Continuously monitors the status of MTA service to see whether a line is delayed or not.
    * When a line transitions from not delayed → delayed, you should print the following message to console or to a logfile: “Line <line_name> is experiencing delays”.
    * Similarly, when a line transitions from delayed → not delayed, you should print the following message to console or to a logfile: “Line <line_name> is now recovered”.
* Exposes an endpoint called /status, which takes the name of a particular line as an argument and returns whether or not the line is currently delayed.
* Exposes an endpoint called /uptime, which also takes the name of a particular line as an argument and returns the fraction of time that it has not been delayed since inception.
    * More concretely, “uptime” is defined as 1 - (total_time_delayed / total_time)

## Getting Started
1) clone this repo locally
2) cd into project dir with Dockerfile and run...
```docker-compose up --build```
3) Use cli cmd to create tables in postgres db
```docker-compose exec api mta_tracker db reset```
4) (Optional) check to see tables have been created in postgres db
```docker-compose exec postgres psql -U mta_tracker -d mta_tracker```
5) Start celery web scraping worker (runs every min)

## Clean up
```docker-compose stop```
```docker-compose rm -f```
```docker rmi -f $(docker images -qf dangling=true)```

## Known Issues
* Celery config should be derived from flask config so instance folder can be used

