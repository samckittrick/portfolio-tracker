#
# PriceDB object controls access to the influxdb price table.
#
#
from datetime import datetime, timezone, timedelta
import yfinance
from influxdb import InfluxDBClient, DataFrameClient, InfluxDBClient

class PriceDB:
    """Object for controlling access to the influxdb price measurement/table. """

    def __init__(self, db_host, db_port, db_name):
        self.hostname = db_host
        self.port = db_port
        self.db_name = db_name
        self.measurement = "price"

        self.fieldTypes = {
            'Dividends': 'float',
            'Close': 'float',
            'High': 'float',
            'Low': 'float',
            'Open': 'float',
            'Stock Splits': 'int',
            'Volume': 'int'
        }

    #--------------------------------------------------
    def updateStockPrice(self, symbol):
        """ Given a particular symbol and the price database"""

        # Get the most recent entry so we can download just the new information
        latest = self.getLatestMeasurement(symbol)
        if(latest == None):
            currentTime = datetime.now(tz=timezone.utc)
            start = currentTime - timedelta(days=60)
        else:
            timestamp = latest['time']
            lastTime = datetime.fromtimestamp(timestamp, timezone.utc)
            start = lastTime

        print(start)
        # Download History
        dfClient = DataFrameClient(host=self.hostname, port=self.port, database=self.db_name)

        ticker = yfinance.Ticker(symbol)
        history = ticker.history(start=start, interval='15m')

        # If there was no history
        if(len(history.index) == 0):
            print("No history available")
            return None

        writeable = history.astype(self.fieldTypes)

        tags = { "symbol": symbol}

        dfClient.write_points(writeable, measurement="price", tags=tags)
        return None

    #----------------------------------------------------------
    def getLatestMeasurement(self, symbol):
        """ Get the latest timestamp for a given symbol and returns it with seconds precision"""
        queryString = "select * from \"price\" where \"symbol\" = $symbol order by time desc limit 1"
        bindParams = { 'symbol': symbol }

        iClient = InfluxDBClient(host=self.hostname, port=self.port, database=self.db_name)
        r = iClient.query(queryString, bind_params=bindParams, epoch="s")

        try:
            return next(r.get_points())
        except:
            return None
