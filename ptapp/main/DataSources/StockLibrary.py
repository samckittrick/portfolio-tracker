#
# Module for collecting, storing, and retrieving stock information.
#
from abc import ABC, abstractmethod
import pandas as pd

################################################################################
# DataSource
################################################################################
class DataSource(ABC):
    """
    Interface representing a data source for the StockLibrary
    """
    #--------------------------------------------------------------------------#
    @abstractmethod
    def get_name(self):
        """
        Get the name of the data source
        """
        pass

################################################################################
# DataSource_Price
################################################################################
class DataSource_Price(DataSource):
    """
    Interface representing a price data source for the StockLibrary
    """
    #--------------------------------------------------------------------------#
    @abstractmethod
    def get_current_price(self, ticker: str) -> dict:
        """
        Get prices for the listed ticker
        """
        pass

################################################################################
# StockLibrary
################################################################################
class StockLibrary:
    """
    Class representing the body of stock data available in the application.
    Has configurable data sources. Future development may include configurable
     storage back ends.
    """

    #--------------------------------------------------------------------------#
    def __init__(self, ds_price: DataSource_Price):
        """
        @param ds_price - DataSource_Price - The data source object for getting stock price data.
        """
        # The object that represents the stock price data source.
        if(isinstance(ds_price, DataSource_Price)):
            self.ds_price = ds_price
        else:
            raise TypeError("Price data source is wrong type. Expected: DataSource_Price Got: %s" % type(ds_price))

    #--------------------------------------------------------------------------#
    def getCurrentStockPrices(self, ticker: str) -> pd.DataFrame:
        """
        Gets the currently known stock prices for a given ticker
        @param ticker - The ticker symbol of the stock
        @return DataFrame containing the stock price data
        """
        return self.ds_price.get_current_price(ticker)
