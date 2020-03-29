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
    return current_app.config['CELERY_RESULT_VALUE']

@celery.task(bind=True)
def updateStock_task(self, symbol):
    dfClient = DataFrameClient(host='192.168.0.250', port=8086, database='stockticker')

    ticker = yfinance.Ticker(symbol)
    history = ticker.history(period='60d', interval='15m')

    colTypes = { 'Dividends': 'float' }
    writeable = history.astype(colTypes)

    tags = { "symbol": symbol}

    dfClient.write_points(writeable, measurement="price", tags=tags)
