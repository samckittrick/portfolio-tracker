from django.db import models
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
    balance = models.DecimalField(max_digits=13, decimal_places=2)

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
            models.UniqueConstraint(fields = [ 'account', 'ftid' ], name="unique transaction")
        ]

    def __str__(self):
        return "%s : %s : %s" % (self.ftid, self.memo, self.amount)
