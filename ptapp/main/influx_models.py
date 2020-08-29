import pandas as pd
import numpy as np
from pandas_schema import Column, Schema
from pandas_schema.validation import *

# InfluxModels are defined and managed using pandas data frames

class StockPrice:
    """
    Model representing stock prices over time
    """

    fieldSchema = Schema([
        Column('open', [IsDtypeValidation(np.float64)]),
        Column('close', [IsDtypeValidation(np.float64)]),
        Column('high', [IsDtypeValidation(np.float64)]),
        Column('low', [IsDtypeValidation(np.float64)]),
        Column('volume', [IsDtypeValidation(np.int64)])
    ])
