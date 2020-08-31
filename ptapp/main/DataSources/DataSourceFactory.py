################################################################################
# Functions for configuring datasources according to django configuration
################################################################################
from . import StockLibrary, ds_yahooquery

#------------------------------------------------------------------------------#
def get_StockLibrary():
    """
    Return a configured StockLibrary object
    """
    # TODO: Make this read from django configuration
    slib_config = {
        'ds_price': ds_yahooquery.DS_YahooQuery()
    }

    return StockLibrary.StockLibrary(**slib_config)
