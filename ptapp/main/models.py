from django.db import models
from .types import InvestmentTransactionTypes, InvestmentTransactionIncomeTypes
# Create your models here.

#################################################
#Describes a particular account being tracked.
##################################################
class Accounts(models.Model):
    CASH_TYPE = "cash"
    CD_TYPE = "cd"
    BOND_TYPE = "bond"
    STOCK_TYPE = "stock"

    typeChoices = [
        (CASH_TYPE, "Cash Account"),
        (CD_TYPE, "Certificate of Deposit"),
        (BOND_TYPE, "Bond"),
        (STOCK_TYPE, "Stock")
    ]

    name = models.CharField(max_length=200)
    account_id = models.CharField(max_length=22)
    institution_name = models.CharField(max_length=200)
    institution_id = models.CharField(max_length=32)
    routing_number = models.CharField(max_length=9)
    currency_symbol = models.CharField(max_length=3)
    type = models.CharField(max_length=6, choices = typeChoices, default=CASH_TYPE)
    accountActive = models.BooleanField(default=True)

    # ------------------------------------------------------------------------
    def __str__(self):
        return "%s at %s" % (self.name, self.institution_name)

    #-------------------------------------------------------------------------
    def getSubclass(self):
        """
        return an instance of the correct subclass according to the account type
        This is based on multi table inheritance
        https://docs.djangoproject.com/en/3.0/topics/db/models/#multi-table-inheritance
        """
        if((self.type == self.CASH_TYPE) or (self.type == self.CD_TYPE)):
            return self.cashaccounts
        else:
            raise NotImplementedError()

    #--------------------------------------------------------------------------
    def getValue(self):
        """
        Get the value of this account as calculated by its subclass
        """
        return self.getSubclass().calculateValue()

    #--------------------------------------------------------------------------
    def calculateValue(self):
        raise NotImplementedError("Cannot calculate value on Account class")

##############################################
# AccountAliases - Store any aliases that an account might have
##############################################
class AccountAliases(models.Model):
    account = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    alias = models.CharField(max_length=200)

################################################################################
# CashAccounts - Subclass for cash accounts specifically
################################################################################
class CashAccounts(Accounts):
    # The main thing we need to consider is the current balance of the account
    balance = models.DecimalField(max_digits=13, decimal_places=2)
    # We also need to know when the balace was updated, so only newer statements
    #  will be used to update it.
    balance_date = models.DateTimeField()

    #--------------------------------------------------------------------------#
    def calculateValue(self):
        return self.balance

################################################################################
# CashTransaction - Specific form of transaction representing a cash transaction
################################################################################
class CashTransaction(models.Model):

    account = models.ForeignKey(CashAccounts, on_delete=models.CASCADE, related_name="transactions")

    date = models.DateTimeField()
    amount = models.FloatField()
    memo = models.CharField(max_length = 255)
    ftid = models.CharField(max_length = 255)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields = [ 'account', 'ftid' ], name="unique cash transaction")
        ]

    def __str__(self):
        return "%s : %s : %s" % (self.ftid, self.memo, self.amount)

################################################################################
# InvestmentAccount - Subclass for investment accounts specifically
################################################################################
class InvestmentAccounts(Accounts):
    # We need to know when the
    position_date = models.DateTimeField()

################################################################################
# InvestmentPositions - List of security positions for a specific account.
###############################################################################
class InvestmentPosition(models.Model):

    account = models.ForeignKey(InvestmentAccounts, on_delete=models.CASCADE, related_name="positions")

    ticker = models.CharField(max_length=8)
    CUSIP = models.CharField(max_length=16)

    # Depending on the broker, it's possible to hold partial shares. So we use a float.
    units = models.FloatField()
    unit_price = models.FloatField()


################################################################################
# InvestmentTransaction
################################################################################
class InvestmentTransaction(models.Model):


    account = models.ForeignKey(InvestmentAccounts, on_delete=models.CASCADE, related_name="transactions")
    ftid = models.CharField(max_length=255)
    type = models.IntegerField(choices = InvestmentTransactionTypes.choices(), default = InvestmentTransactionTypes.BUY_OTHER)
    tradeDate = models.DateTimeField()
    settleDate = models.DateTimeField()
    memo = models.CharField(max_length=255)
    CUSIP = models.CharField(max_length=16)
    ticker = models.CharField(max_length=8)
    income_type = models.IntegerField(choices = InvestmentTransactionIncomeTypes.choices())
    units = models.FloatField()
    unit_price = models.FloatField()
    comission = models.FloatField()
    fees = models.FloatField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields = [ 'account', 'ftid' ], name="unique investment transaction")
        ]
