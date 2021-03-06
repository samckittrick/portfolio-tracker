# portfolio-tracker
Application to track my stock portfolio. Also as a python,flask,investing learning project.

Running with Docker Compose  
`sudo docker-compose --file portfolio-tracker-compose.yml up`

Running the celery worker outside of Docker (requires docker compose ports to be exported)  
`env $(cat config/container.env | grep -v "#" | xargs) celery worker -A celery_worker.celery --loglevel=info`

Running the flask app from outside Docker  
`env $(cat config/container.env | grep -v "#" | xargs) FLASK_APP=flaskapp.py flask run --host=0.0.0.0 --port=8000`

## Configuration
Configuration takes a number of steps that will be progressively automated as I move forward. In theory most of this
 configuration will be one time and can be done with a bootstrapping script.

Configuration for each service has it's own folder in the config directory.

**mariadb configuration**  
mariadb is initially configured using environment variables that are found in config/mariadb/mariadb.env. This provides the root
password, initial user and stocks database. The variables are provided to the container by docker-compose.

Additional scripts and sql files are mounted at /docker-endpoint-initdb.d to provision the database further.  These are automatically run by the container on first launch in order to create and populate the stocks database.

**influxdb configuration**  
Influxdb is configured using files in the config/influxdb directory.   

Currently, I do not create a root password, user or user password. This will likely change in the future and will follow the same
path as mariadb, using environment variables for initial configuration.

Influxdb maintains the same entrypoint feature as mariadb and the configuration directory is mounted at /docker-endpoint-initdb.d
where influxdb can read the provided scripts and iql file to create and configure the appropriate database.

**Flask api configuration**  
Flask and celery can be configured using two different methods. A config file or environment variables.
The config file path is specified using the environment variable `PTAPP_CONFIG`. I think this could be changed to use a custom loader and a command line parameter, but I'm not sure yet. The config file is written in yaml.     
Example:
```
redis:
  hostname: 192.168.0.250
  port: 6379
  databaseId: 0

influxdb:
  hostname: 192.168.0.250
  port: 8086
  databaseName: stockticker
```

Environment variables provided to the application override corresponding values in the configuration file. This allows us to keep a config file for testing flask outside of docker, while providing all the hostnames and such we need through environment variables in the docker-compose file.   
The below is a list of variables you can use:
```
PTAPP_REDIS_HOSTNAME - Hostname of the redis instance
PTAPP_REDIS_PORT - port that the redis instance is listening on
PTAPP_REDIS_DBID - database id to use in the redis database
PTAPP_INFLUXDB_HOSTNAME - hostname of the influxdb database
PTAPP_INFLUXDB_PORT - port for accessing the influxdb database
PTAPP_INFLUXDB_DBNAME - the name of the influxdb database
```

**Grafana configuration**  
Grafana can be configured using a series of files in the config directory. Preprovisioned dashboards are provided.   
+ [Provisioning](https://grafana.com/docs/grafana/latest/administration/provisioning/)  
+ [Configure Grafana Docker Image](https://grafana.com/docs/grafana/latest/installation/configure-docker/)

## Docker Compose Configuration
-------
Configuration happens through a series of environment variables. These are passed to containers by docker-compose. The following parameters exist:  

**.env file** For use by docker-compose
```
PORTFOLIO_TRACKER_DIR=/home/wallace/portfolio-tracker/testpersistentdir/
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
