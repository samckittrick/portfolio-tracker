#
# This module imports and creates a celery application. It should be called to create a celery worker
#
from ptapp import celery,create_app
from config import Config

config = Config()
# We are creating a flask context as well so that the tasks have access to it?
app = create_app(config)
# https://flask.palletsprojects.com/en/1.0.x/appcontext/
app.app_context().push()
