from .StockLibrary import DataSource_Price
from yahooquery import Ticker

################################################################################
# DataSource for Yahoo Query
class DS_YahooQuery(DataSource_Price):
    """
    yahooquery datasource. Accesses yahoo finance api
    """

    #--------------------------------------------------------------------------#
    def get_name(self):
        return "DS_YahooQuery"

    #--------------------------------------------------------------------------#
    def get_current_price(self, ticker: str):
        """
        Get the current price data for a given ticker symbol
        """
        tickerObj = Ticker(ticker)
        pdata = tickerObj.price[ticker]

        # If the price is a string, it means we couldn't get the data.
        # yahooquery does not throw an error when that happens
        if(isinstance(pdata, str)):
            print("No data for %s. Fix me!" % ticker)
            return None

        priceData = {
            'ticker': ticker,
            'name': pdata['shortName'],
            'price': pdata['regularMarketPrice']
        }

        if(pdata['quoteType'] == "EQUITY"):
            priceData.update({
                'dayhigh': pdata['regularMarketDayHigh'],
                'daylow': pdata['regularMarketDayLow'],
                'dayvolume': pdata['regularMarketVolume'],
                'dayopen': pdata['regularMarketOpen'],
                'currency': pdata['currency']
            })
        return priceData
