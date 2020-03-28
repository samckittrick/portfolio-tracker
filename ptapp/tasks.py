#
# Module for defining long running celery tasks
#

from . import celery
import time

@celery.task(bind=True)
def long_task(self):
    print("Long Task")
    self.update_state(state='STARTED', meta={'value': "hello"})
    time.sleep(20)
    raise NotImplementedException
    self.update_state(state='PROGRESS', meta={'value': "Still Working"})
    time.sleep(20)
    return "I Finished!"
