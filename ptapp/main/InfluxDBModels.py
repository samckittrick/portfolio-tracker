from influxable.measurement import Measurement
from influxable import attributes
#
# Define models for influxdb access.
# We use Influxable for this since the django orm doesn't support it.
#

class CashTransaction(Measurement):
    measurement_name = 'CashTransaction'

    # Fields
    # Date of the transaction
    transactionDate = attributes.TimestampFieldAttribute()
    #The amount of the transaction
    amount = attributes.FloatFieldAttribute()

    #Tags
    # Description of the transaction
    memo = attributes.TagFieldAttribute()
    # Financial Institution specific transaction id
    fi_id = attributes.TagFieldAttribute()
    # Account ID
    account = attributes.TagFieldAttribute()
