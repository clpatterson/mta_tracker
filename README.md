# MTA Tracker
![GitHub Actions status | integration-tests](https://github.com/clpatterson/mta_tracker/workflows/integration-tests/badge.svg)

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
2) cd into project dir with Dockerfile and run... (Note: celery worker is started right away)
```
docker-compose up --build
```
3) In another terminal window, use cli cmd to create tables in postgres db
```
docker-compose exec api mta_tracker db reset
```
4) (Optional) check to see tables have been created in postgres db
```
docker-compose exec postgres psql -U mta_tracker -d mta_tracker
```
6) Ping the status endpoint for a subway line's status
```
http://localhost:8000/mta_tracker/api/v1.0/subway/lines/status?line=L
```
7) Ping the uptime endpoint for a subway line's uptime
```
http://localhost:8000/mta_tracker/api/v1.0/subway/lines/uptime?line=L
```
8) Check logs for messages related to subway line status changes
```
docker-compose exec api cat logs/line_status.log
```

## Testing
* Run the following command to test endpoints
```bash
docker-compose exec api py.test mta_tracker/tests
```

## Clean up
```
docker-compose stop
```
```
docker-compose rm -f
```
```
docker rmi -f $(docker images -qf dangling=true)
```

## Implementation details
* A celery worker runs the task in mta_tracker/tasks/tasks.py every minute.
All details regarding the continuous monitoring of MTA service status can be
found in that file, including logging and where data is stored in the db.
* To understand endpoints, see mta_tracker/resources/subway/lines.py.

## Known Issues
* Celery config should be stored in same file as flask configs...this way
instance folder can be used for prod configs. 
* Times are all in UTC

