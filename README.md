# portfolio-tracker
Application to track my stock portfolio. Also as a python,flask,investing learning project.

Running with Docker Compose  
`sudo docker-compose --file portfolio-tracker-compose.yml up`

Running the celery worker outside of Docker (requires docker compose ports to be exported)  
`env $(cat config/container.env | grep -v "#" | xargs) celery worker -A celery_worker.celery --loglevel=info`

Running the flask app from outside Docker  
`env $(cat config/container.env | grep -v "#" | xargs) FLASK_APP=flaskapp.py flask run --host=0.0.0.0 --port=8000`

## Configuration
Configuration takes a number of steps that will be progressively automated as I move forward.

**mariadb configuration**  
mariadb is initially configured using environment variables that are found in container.env. This will eventually be created using a bootstrap script
Additional scripts and sql files are mounted at /docker-endpoint-initdb.d to provision the database further.  These are automatically run by the container on first launch.

**influxdb configuration**  
Influxdb currently needs no configuration, but it maintains the same entrypoint feature as mariadb.

**Grafana configuration**
Grafana can be configured using a series of files in the config directory.
[Provisioning](https://grafana.com/docs/grafana/latest/administration/provisioning/)
[Configure Grafana Docker Image](https://grafana.com/docs/grafana/latest/installation/configure-docker/)

**Previous:**  
-------
Configuration happens through a series of environment variables. These are passed to containers by docker-compose. The following
parameters exist:  

**.env file** For use by docker-compose
```
PORTFOLIO_TRACKER_DIR=/home/wallace/portfolio-tracker/testpersistentdir/
```

**container.env** To be passed to containers  
Some of this will need to be marked "do not change"
```
REDIS_HOSTNAME=localhost
REDIS_PORT=6379
REDIS_DB=0

MYSQL_ROOT_PASSWORD=mysecretpass
MYSQL_DATABASE=stocksdb
MYSQL_USER=stocksdb_user
MYSQL_PASSWORD=stocksdb_password
```


## References

### Application Structure
I struggled quite a bit with structuring the application properly to avoid circular imports. Flask and Celery aren't easy to make work while you are still learning
them. I borrowed heavily from several blog posts and a git repo by Miguel Grinberg
- [Using Celery with Flask](https://blog.miguelgrinberg.com/post/using-celery-with-flask)
- [Celery and the Flask Application Factory Pattern](https://blog.miguelgrinberg.com/post/celery-and-the-flask-application-factory-pattern)
- [Flasky with Celery Github Repo](https://github.com/miguelgrinberg/flasky-with-celery)

### Environment variables
Since this project will eventually be started using docker compose and different containers will need to share
some of the same configuration values, we pass most of the configuration through environment variables. For testing,
this means a lot of typing. A solution is to place all the environment variables in a file and read them right before
launching the test server using this command: `env $(cat container.env | grep -v "#" | xargs) commandToBeRun`

This came from [Injecting Environment Variables from a file with xargs](https://www.mokacoding.com/blog/env-xargs/)
