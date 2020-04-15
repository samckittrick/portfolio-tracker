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

    #---------------------------------------------------------
    def __getDFConnection(self):
        """ Get a dataframe connection object"""
        return DataFrameClient(host=self.hostname, port=self.port, database=self.db_name)

    #---------------------------------------------------------
    def __getConnection(self):
        """Get a normal influxdb connection"""
        return InfluxDBClient(host=self.hostname, port=self.port, database=self.db_name)

    #--------------------------------------------------
    def updateStockPrice_Dataframe(self, symbol, frame):
        """ Given a dataframe of data, update the price db for a specific symbol"""

        # Insert data frame
        dfClient = self.__getDFConnection()
        writeable = frame.astype(self.fieldTypes)

        tags = { "symbol": symbol}

        dfClient.write_points(writeable, measurement="price", tags=tags)
        return None

    #----------------------------------------------------------
    def getLatestMeasurement(self, symbol):
        """ Get the latest timestamp for a given symbol and returns it with seconds precision"""
        queryString = "select * from \"price\" where \"symbol\" = $symbol order by time desc limit 1"
        bindParams = { 'symbol': symbol }

        iClient = self.__getConnection()
        r = iClient.query(queryString, bind_params=bindParams, epoch="s")

        try:
            return next(r.get_points())
        except:
            return None
