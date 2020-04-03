#
# Module for defining long running celery tasks
#

from . import celery
import time
from flask import current_app
from .PriceDB import PriceDB

#--------------------------------------------------------------
@celery.task(bind=True)
def long_task(self):
    print("Long Task")
    self.update_state(state='STARTED', meta={'value': "hello"})
    time.sleep(20)
    self.update_state(state='PROGRESS', meta={'value': "Still Working"})
    time.sleep(20)
    return "Done!"

#------------------------------------------------------------------
@celery.task(bind=True)
def updateStock_task(self, symbol):
    hostname = current_app.config['influxdb_hostname']
    port = current_app.config['influxdb_port']
    database = current_app.config['influxdb_dbName']

    db = PriceDB(hostname, port, database)
    db.updateStockPrice(symbol)
