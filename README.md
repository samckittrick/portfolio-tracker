# portfolio-tracker
Application to track my stock portfolio. Also as a python,flask,investing learning project.  
![CI workflow](https://github.com/samckittrick/portfolio-tracker/workflows/CI%20workflow/badge.svg)

**Running with Docker Compose**  (This needs more work still)  
This is a multistep process, depending on what needs to be done.
1. Build the container `sudo docker build -t foo .`
2. Run the docker compose file to start up database services. Later I will pull this container into compose too.
3. Run the container for initial set up steps (do this the first time)
```
wallace@grommit:~/portfolio-tracker$ sudo docker run --rm --network host -it foo /bin/bash
root@grommit:/opt/app# cd /opt/app/ptapp
root@grommit:/opt/app/ptapp# python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, imports, main, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying main.0001_initial... OK
  Applying imports.0001_initial... OK
  Applying sessions.0001_initial... OK
root@grommit:/opt/app/ptapp# python manage.py createsuperuser
Username (leave blank to use 'root'): admin
Email address:
Password:
Password (again):
Superuser created successfully.
root@grommit:/opt/app/ptapp# exit
```  
4. Rerun the container to start the server `sudo docker run --rm --network host -it foo`


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

## Development and Testing
For testing and development, you need to install a few extra requirements
```
pip install -r devrequirements.txt
```

## Building Bootstrap with custom themes
In order to build a custom themed bootstrap, I place `custom.scss` in the boostrap directory. Then I modify the `css-compile` task in `packages.json` to point to custom.css instead of bootstrap.css. Once you run `npm run dist` or `npm run css` the resultant css and minified css files are in the dist directory.
