#
# This module imports and creates a celery application. It should be called to create a celery worker
#
from ptapp import celery,create_app
from config import Config
from celery.schedules import crontab

config = Config()

schedule = {
    'updateAll': {
        'task': 'ptapp.tasks.updateAllStockPrices_task',
        'schedule': crontab(minute="*")
    }
}
config.setConfig('beat_schedule', schedule)
# We are creating a flask context as well so that the tasks have access to it?
app = create_app(config)
# https://flask.palletsprojects.com/en/1.0.x/appcontext/
app.app_context().push()
