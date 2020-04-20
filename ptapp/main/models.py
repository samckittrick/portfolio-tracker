from django.db import models

# Create your models here.

#Describes a particular account being tracked.
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

    def __str__(self):
        return "%s at %s" % (self.name, self.institution_name)

#Store any aliases that an account might have
class AccountAliases(models.Model):
    account = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    alias = models.CharField(max_length=200)

# Temporary table storing imported account information
class FileImportAccountData(models.Model):

    #need some id to idendtify the upload. for now use the django provided auto increment key
    friendlyName = models.CharField(max_length = 200, default='')
    account_id = models.CharField(max_length=22)
    routing_number = models.CharField(max_length=9)
    institution_name = models.CharField(max_length=200)
    institution_id = models.CharField(max_length=32)
    type = models.CharField(max_length = 6, choices = Accounts.typeChoices, default=Accounts.CASH_TYPE)
    balance = models.DecimalField(max_digits=13, decimal_places=2)
    balance_date = models.DateTimeField()
    currency_symbol = models.CharField(max_length=3)
    matched = models.BooleanField(default=False)
    matched_account_id = models.ForeignKey(Accounts, on_delete=models.CASCADE, null=True)
