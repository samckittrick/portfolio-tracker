from influx_models import StockPrice
import pandas as pd

data = {
    'ticker': ["yh", "sa"]
}

df = pd.DataFrame(data)
print(df.dtypes)
result = StockPrice.fieldSchema.validate(df)
for error in result:
    print(error)
