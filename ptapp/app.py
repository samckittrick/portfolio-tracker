#
# Module for creating and managing celery applications.
#
from celery import Celery
from celery.signals import after_setup_logger

from flask import Flask

from .config import Config

import logging
import sys

#In order to register the blueprints, we must list them here
from .main_routes import main_routes

#In order to register celery tasks, we must list their modules here.
# If we add more tasks in other modules or submodules, we add them to the list here.
CELERY_TASK_LIST = [
    "ptapp.tasks"
]

mConfig = Config()
cConfig = mConfig.get_celery_config()

############################################
# Create the flask app
############################################
flaskApp = Flask(__name__)

flaskApp.config['CELERY_BROKER_URL'] = cConfig.CELERY_BROKER_URL
flaskApp.config['CELERY_RESULT_BACKEND'] = cConfig.CELERY_RESULT_BACKEND

# Register blueprints so we can write them in other files and prevent clutter
flaskApp.register_blueprint(main_routes)

#############################################
# Create and configure the celery application
#############################################

logger = logging.getLogger(__name__)

celery = Celery(__name__, broker=cConfig.CELERY_BROKER_URL, include=CELERY_TASK_LIST)
celery.config_from_object(cConfig)
#celery.autodiscover_tasks(CELERY_TASK_LIST)

#Logging configuration
# https://www.distributedpython.com/2018/08/28/celery-logging/
@after_setup_logger.connect
def setup_loggers(logger, *args, **kwargs):
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
