# RoboFleet_JustLearning

/robots
/maintenance-tasks
/jobs

Each robot can be doing a specific job at a given time
CRUD allowed on all 3 endpoints

Run `docker build -t robo-fleet-server .` to build image on your machine
Run `docker run -d -p 8000:8000 --name robo-fleet-server robo-fleet-server` to run the image in docker