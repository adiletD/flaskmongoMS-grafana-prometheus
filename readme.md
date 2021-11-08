# Overview

This application is containerized python flask REST API using Mongo DB (running as a docker container) as the backend database server.

# Installtion and launch

## Launching the containers

To launch the network of containers we are using

`docker-compose up`

This command will launch all the microservices and we can start the testing

`pytest unit.py`

# Files

- Docker-compose file for launching the various containers (Your python flask app, mongodb, prometheus, grafana)
- A folder named "student_service" with your python flask app and Dockerfile for building your student service.
- A folder named "tests" with a python script unit.py for unit testing your python flask app using pytest (by submitting HTTP requests to the different endpoints in the student_service container).
- A prometheus.yml defining the Prometheus configuration with the endpoint to scrape the metric.
- A folder named "grafana" with your dashboard and Grafana’s startup configuration
- readme.md: Provide instructions of how to launch your app and access the various services and run your unit tests.
