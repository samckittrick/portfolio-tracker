#
# Module for defining long running celery tasks
#

from .app import celery

@celery.task(bind=True)
def long_task(self):
    print("Long Task")
    self.update_state(state='STARTED', meta={'value': "hello"})
    time.sleep(20)
    self.update_state(state='PROGRESS', meta={'value': "Still Working"})
    time.sleep(20)
    return "I Finished!"
