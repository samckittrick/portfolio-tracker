#
# This script is intended to test pulling data down from the yfinance api and inserting it into the influxdb for display by grafana
#

import yfinance
from influxdb import InfluxDBClient, DataFrameClient

stockList = [ '^DJI', 'AAPL', 'UNP', 'TEAM' ]
#stockList = [ '^DJI' ]


# Lets Create the database first
client = InfluxDBClient(host="192.168.0.250", port=8086)
client.create_database('stocks')
client.switch_database('stocks')

dfClient = DataFrameClient(host='192.168.0.250', port=8086, database='stocks')

for s in stockList:
    ticker = yfinance.Ticker(s)
    history = ticker.history(period='60d', interval='15m')

    # Sometimes the dividend comes back as a 0 which makes the autodetect think it's an int. This might cause the write to fail if the field
    #   has already been writen as a float or later when something tries to write it as a float
    colTypes = { 'Dividends': 'float' }
    writeable = history.astype(colTypes)

    tags = { "symbol": s }
        
    dfClient.write_points(writeable, measurement="price", tags=tags)
