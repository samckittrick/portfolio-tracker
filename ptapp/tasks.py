#
# Module for defining long running celery tasks
#

from . import celery
import time
from flask import current_app

import yfinance
from influxdb import InfluxDBClient, DataFrameClient

@celery.task(bind=True)
def long_task(self):
    print("Long Task")
    self.update_state(state='STARTED', meta={'value': "hello"})
    time.sleep(20)
    self.update_state(state='PROGRESS', meta={'value': "Still Working"})
    time.sleep(20)
    return "Done!"

@celery.task(bind=True)
def updateStock_task(self, symbol):
    hostname = current_app.config['influxdb_hostname']
    port = current_app.config['influxdb_port']
    database = current_app.config['influxdb_dbName']
    dfClient = DataFrameClient(host=hostname, port=port, database=database)

    ticker = yfinance.Ticker(symbol)
    history = ticker.history(period='60d', interval='15m')

    colTypes = { 'Dividends': 'float' }
    writeable = history.astype(colTypes)

    tags = { "symbol": symbol}

    dfClient.write_points(writeable, measurement="price", tags=tags)
