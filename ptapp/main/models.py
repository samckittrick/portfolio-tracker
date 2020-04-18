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
    bank = models.CharField(max_length=200)
    type = models.CharField(max_length=6, choices = typeChoices, default=CASH_TYPE)
    
    def __str__(self):
        return "%s at %s" % (self.name, self.bank)

#Store any aliases that an account might have
class AccountAliases(models.Model):
    account = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    alias = models.CharField(max_length=200)
