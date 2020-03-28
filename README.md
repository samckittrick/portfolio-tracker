# portfolio-tracker
Application to track my stock portfolio. Also as a python,flask,investing learning project.

Running with Docker Compose  
`sudo docker-compose --file portfolio-tracker-compose.yml up`

Running the celery worker outside of Docker (requires docker compose ports to be exported)  
`celery worker -A celery_worker.celery --loglevel=info`

Running the flask app from outside Docker  
`FLASK_APP=flaskapp.py flask run --host=0.0.0.0 --port=8000`

## References
I struggled quite a bit with structuring the application properly to avoid circular imports. Flask and Celery aren't easy to make work while you are still learning
them. I borrowed heavily from several blog posts and a git repo by Miguel Grinberg
- [Using Celery with Flask](https://blog.miguelgrinberg.com/post/using-celery-with-flask)
- [Celery and the Flask Application Factory Pattern](https://blog.miguelgrinberg.com/post/celery-and-the-flask-application-factory-pattern)
- [Flasky with Celery Github Repo](https://github.com/miguelgrinberg/flasky-with-celery)
