#
# Module for defining long running celery tasks
#

from . import celery
import time
from flask import current_app

@celery.task(bind=True)
def long_task(self):
    print("Long Task")
    self.update_state(state='STARTED', meta={'value': "hello"})
    time.sleep(20)
    self.update_state(state='PROGRESS', meta={'value': "Still Working"})
    time.sleep(20)
    return current_app.config['CELERY_RESULT_VALUE']
