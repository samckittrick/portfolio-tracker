################################################################################
# Testing the StockLibrary class
################################################################################
import unittest

from main.DataSources.StockLibrary import StockLibrary, DataSource_Price

################################################################################
# MockDataSourceFactory
################################################################################
class MockDataSourceFactory:
    """
    Generates a mock data source object and returns it plus the data contained
    """

    #--------------------------------------------------------------------------#
    @staticmethod
    def getDataSourcePrice():
        """
        Generate a datasource_price object
        """
        data = {
            'aapl': {
                'ticker': 'aapl',
                'price': 499.23,
                'dayhigh': 505.75,
                'daylow': 498.32,
                'dayvolume': 46907479,
                'dayopen': 504.05
            },
            'team': {
                'ticker': 'team',
                'price': 123.45,
                'dayhigh': 543.21,
                'daylow': 21.56,
                'dayvolume': 123456,
                'dayopen': 504.05
            }
        }

        class mock_DataSource_Price(DataSource_Price):
            def __init__(self, data):
                self.data = data
            def get_name():
                return "mock_DataSource_Price"
            def get_current_price(self, ticker):
                return data[ticker]
        return mock_DataSource_Price(data), data



################################################################################
# TestStockLibrary
################################################################################
class TestStockLibrary(unittest.TestCase):
    """ For testing the StockLibrary class"""

    #--------------------------------------------------------------------------#
    def testGetCurrentPrice(self):
                dsp, data = MockDataSourceFactory.getDataSourcePrice()
                slib = StockLibrary(ds_price=dsp)

                currentPriceData = slib.getCurrentStockPrices('aapl')
                self.assertDictEqual(currentPriceData, data['aapl'])
                currentPriceData = slib.getCurrentStockPrices('team')
                self.assertDictEqual(currentPriceData, data['team'])
