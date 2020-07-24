# portfolio-tracker
Application to track my stock portfolio. Also as a python,flask,investing learning project.

![CI workflow](https://github.com/samckittrick/portfolio-tracker/workflows/CI%20workflow/badge.svg)

**Running with Docker Compose**  
`sudo docker-compose --file portfolio-tracker-compose.yml up`

**Running the Django App Separately**  
```
wallace@grommit:~/portfolio-tracker$ source venv/bin/activate
(venv) wallace@grommit:~/portfolio-tracker$ cd ptapp
(venv) wallace@grommit:~/portfolio-tracker/ptapp$ python manage.py runserver 0:8000
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
April 18, 2020 - 04:17:35
Django version 3.0.5, using settings 'ptapp.settings'
Starting development server at http://0:8000/
Quit the server with CONTROL-C.
```

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


## Docker Compose Configuration
-------
Configuration happens through a series of environment variables. These are passed to containers by docker-compose. The following parameters exist:  

**.env file** For use by docker-compose
```
PORTFOLIO_TRACKER_DIR=/home/wallace/portfolio-tracker/testpersistentdir/
```

## Building Bootstrap with custom themes
In order to build a custom themed bootstrap, I place `custom.scss` in the boostrap directory. Then I modify the `css-compile` task in `packages.json` to point to custom.css instead of bootstrap.css. Once you run `npm run dist` or `npm run css` the resultant css and minified css files are in the dist directory.
