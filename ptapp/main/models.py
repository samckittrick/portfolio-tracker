from django.db import models
import hashlib

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

    def __str__(self):
        return "%s at %s" % (self.name, self.institution_name)

##############################################
#Store any aliases that an account might have
##############################################
class AccountAliases(models.Model):
    account = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    alias = models.CharField(max_length=200)

###############################################################
# Temporary table for storing information about imported files
###############################################################
class FileImport_FileData(models.Model):
    fileid = models.CharField(max_length=32, primary_key=True)
    filename = models.CharField(max_length=200)
    expiration = models.DateTimeField()

    def calculatefilehash(file):
        """ Calculate the hash of a file for inserting into this model"""
        hasher = hashlib.md5()
        for chunk in file.chunks():
            hasher.update(chunk)
        hash = hasher.hexdigest()
        return hash

    def saveNewFile(fileHash):
        fileEntry = FileImport_FileData.objects.get(pk=fileHash)
        if(fileEntry.accounts.count() > 1):
            raise Exception("Cannot yet import more than one account!")
        elif(fileEntry.accounts.count() == 0):
            raise Exception("File does not have any associated accounts")

        account = fileEntry.accounts.first()
        accountModel = Accounts()
        if(account.friendlyName != ""):
            accountModel.name = account.friendlyName
        else:
            accountModel.name = account.account_id
        accountModel.account_id = account.account_id
        accountModel.institution_name = account.institution_name
        accountModel.institution_id = account.institution_id
        accountModel.routing_number = account.routing_number
        accountModel.currency_symbol = account.currency_symbol
        accountModel.type = account.type
        accountModel.save()

        # Once we have done all the saving we need. Delete the file and it's children
        fileEntry.delete()

########################################################
# Temporary table storing imported account information
########################################################
class FileImport_AccountData(models.Model):

    #need some id to idendtify the upload.
    file = models.ForeignKey(FileImport_FileData, on_delete=models.CASCADE, related_name="accounts")

    friendlyName = models.CharField(max_length = 200)
    account_id = models.CharField(max_length=22)
    routing_number = models.CharField(max_length=9)
    institution_name = models.CharField(max_length=200)
    institution_id = models.CharField(max_length=32)
    type = models.CharField(max_length = 6, choices = Accounts.typeChoices, default=Accounts.CASH_TYPE)
    balance = models.DecimalField(max_digits=13, decimal_places=2)
    balance_date = models.DateTimeField()
    currency_symbol = models.CharField(max_length=3)
    matched = models.BooleanField(default=False)
    matched_account_id = models.ForeignKey(Accounts, on_delete=models.CASCADE, null=True, related_name="matched_account")
