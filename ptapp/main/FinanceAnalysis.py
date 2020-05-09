################################################################################
# Module that provides functions for calculating various metrics
################################################################################
from django.db.models import Q
import decimal

from .models import Accounts

def getNetWorth():
    """
    For all accounts in the model calculate the appropriate net worth
    """
    print("Warning: Only Calculating cash and CDs!!!!")
    net_worth = decimal.Decimal(0.00)

    accountList = Accounts.objects.filter(Q(accountActive=True), Q(type=Accounts.CASH_TYPE) | Q(type=Accounts.CD_TYPE))
    for a in accountList:
        net_worth = net_worth + a.balance

    return net_worth
