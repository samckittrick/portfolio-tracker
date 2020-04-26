from django.db import models
import hashlib

from main.models import Accounts

# Create your models here.
###############################################################
# Temporary table for storing information about imported files
###############################################################
class FileData(models.Model):
    fileid = models.CharField(max_length=32, primary_key=True)
    filename = models.CharField(max_length=200)
    expiration = models.DateTimeField()

    #--------------------------------------------------------------------------#
    def calculatefilehash(file):
        """ Calculate the hash of a file for inserting into this model"""
        hasher = hashlib.md5()
        for chunk in file.chunks():
            hasher.update(chunk)
        hash = hasher.hexdigest()
        return hash

    #--------------------------------------------------------------------------#
    def completeImportFile(self):
        """
        Now that the file has been confirmed, transfer the data to the main database.
        """
        for a in self.accounts.all():
            a.completeAccountImport()


########################################################
# Temporary table storing imported account information
########################################################
class AccountData(models.Model):

    #need some id to idendtify the upload.
    file = models.ForeignKey(FileData, on_delete=models.CASCADE, related_name="accounts")

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
    matched_account_id = models.ForeignKey(Accounts, on_delete=models.PROTECT, null=True, related_name="matched_account")

    #--------------------------------------------------------------------------#
    def completeAccountImport(self):
        if(self.matched):
            print("WARNING: Not updating matched account info. Need to decide how to do this")
        else:
            print("Unmatched")
            accountModel = Accounts()
            if(self.friendlyName != ""):
                accountModel.name = self.friendlyName
            else:
                accountModel.name = self.account_id
            accountModel.account_id = self.account_id
            accountModel.institution_name = self.institution_name
            accountModel.institution_id = self.institution_id
            accountModel.routing_number = self.routing_number
            accountModel.currency_symbol = self.currency_symbol
            accountModel.type = self.type
            accountModel.save()
