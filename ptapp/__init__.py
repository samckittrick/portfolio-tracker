from flask import Flask
from celery import Celery
from celery.signals import after_setup_logger
# The config module comes from outside the ptapp package because it is found at the level
# of the flask app and celery worker, both of which are called from the project's root level
from config import config

import logging
import sys

# We create the celery app here so that we don't need to
celery = Celery(__name__, broker=config.CELERY_BROKER_URL)

#logger = logging.getLogger(__name__)

#Logging configuration
# https://www.distributedpython.com/2018/08/28/celery-logging/
#@after_setup_logger.connect
#def setup_loggers(logger, *args, **kwargs):
#    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#    handler = logging.StreamHandler(sys.stdout)
#    handler.setFormatter(formatter)
#    logger.addHandler(handler)

# We hold off on creating the app because doing so will cause circular imports with
# the registration of blueprints
def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    celery.conf.update(app.config)

    from .main_routes import main_routes
    app.register_blueprint(main_routes)

    return app
