#
# Module for defining long running celery tasks
#

from . import celery
import time
from flask import current_app
from .PriceDB import PriceDB
from .StockDB import StockDB
import yfinance
from datetime import datetime, timezone, timedelta

#--------------------------------------------------------------
@celery.task(bind=True)
def long_task(self):
    """Just run a long task to see if it works"""
    print("Long Task")
    self.update_state(state='STARTED', meta={'value': "hello"})
    time.sleep(20)
    self.update_state(state='PROGRESS', meta={'value': "Still Working"})
    time.sleep(20)
    return "Done!"

#------------------------------------------------------------------
@celery.task(bind=True)
def updateStock_task(self, symbol):
    """ Update price information for a particular symbol"""
    print("Updating: %s" % symbol)
    hostname = current_app.config['influxdb_hostname']
    port = current_app.config['influxdb_port']
    database = current_app.config['influxdb_dbName']

    # Get an accessor object instance.
    db = PriceDB(hostname, port, database)

    # Get the most recent price point so we don't re download things we already have
    latest = db.getLatestMeasurement(symbol)
    if(latest == None):
        currentTime = datetime.now(tz=timezone.utc)
        start = currentTime - timedelta(days=60)
    else:
        timestamp = latest['time']
        lastTime = datetime.fromtimestamp(timestamp, timezone.utc)
        start = lastTime

    ticker = yfinance.Ticker(symbol)
    history = ticker.history(start=start, interval='15m')

    # If there was no history
    if(len(history.index) == 0):
        print("No history available")
        return None

    db.updateStockPrice_Dataframe(symbol, history)

#------------------------------------------------------------------
@celery.task(bind=True)
def updateAllStockPrices_task(self):
    """Update price information for all symbols. """
    print("Updating all")
    hostname = current_app.config['mysql_hostname']
    port = current_app.config['mysql_port']
    username = current_app.config['mysql_username']
    password = current_app.config['mysql_password']
    database = current_app.config['mysql_database']

    db = StockDB(hostname, port, database, username, password)

    stocks = db.getTrackedStocks()

    for s in stocks:
        print(type(s))
        updateStock_task.apply_async(args=[s])

    return None
