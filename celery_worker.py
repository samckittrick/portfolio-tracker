#
# This module imports and creates a celery application. It should be called to create a celery worker
#
from ptapp import celery,create_app
from ptapp.tasks import updateAllInformation_task
from config import Config
from celery.schedules import crontab

config = Config()

schedule = {
    'updateAll': {
        'task': 'ptapp.tasks.updateAllInformation_task',
        'schedule': crontab(minute="*/15")
    }
}
config.setConfig('beat_schedule', schedule)
# We are creating a flask context as well so that the tasks have access to it?
app = create_app(config)
# https://flask.palletsprojects.com/en/1.0.x/appcontext/
app.app_context().push()

#Celery beat can't be configured to run a task on startup so we do it here.
updateAllInformation_task.apply_async(countdown=30)
