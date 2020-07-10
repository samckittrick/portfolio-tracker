from django.db import models, transaction
import hashlib

import main
from main.models import CashAccounts, Accounts

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
        with transaction.atomic():
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
    currency_symbol = models.CharField(max_length=3)
    matched = models.BooleanField(default=False)
    matched_account_id = models.ForeignKey(Accounts, on_delete=models.PROTECT, null=True, related_name="matched_account")

    #-------------------------------------------------------------------------
    def getSubclass(self):
        """
        return an instance of the correct subclass according to the account type
        This is based on multi table inheritance
        https://docs.djangoproject.com/en/3.0/topics/db/models/#multi-table-inheritance
        """
        if((self.type == Accounts.CASH_TYPE) or (self.type == Accounts.CD_TYPE)):
            return self.cashaccountdata
        else:
            raise NotImplementedError()

    #--------------------------------------------------------------------------#
    def completeAccountImport(self):
        self.getSubclass().completeAccountImport()

    #--------------------------------------------------------------------------#
    def saveGenericAccountFields(self, accountModel):
        """
        Save the fields that are common to all accounts to the given Accounts object
        """
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

################################################################################
# CashAccountData - Temporary Specific table for cash accounts
################################################################################
class CashAccountData(AccountData):
    balance = models.DecimalField(max_digits=13, decimal_places=2)
    balance_date = models.DateTimeField()

    #--------------------------------------------------------------------------#
    def completeAccountImport(self):
        if(self.matched):
            print("WARNING: Not updating matched account info. Need to decide how to do this.")
            # Get the matched account and get the right type so that we can save to it.
            accountModel = self.matched_account_id.cashaccounts
            print(type(accountModel))
        else:
            accountModel = CashAccounts()
            self.saveGenericAccountFields(accountModel)


        # Update balance of matched or unmatched account
        accountModel.balance = self.balance
        accountModel.balance_date = self.balance_date
        accountModel.save()

        # Whether we matched or not, we also need to import transaction
        for t in self.transactions.all():
            t.completeTransactionImport(accountModel)



################################################################################
# Temporary table for storing imported  Cash Transactions
################################################################################
class CashTransaction(models.Model):

    account = models.ForeignKey(CashAccountData, on_delete=models.CASCADE, related_name="transactions")

    date = models.DateTimeField()
    amount = models.FloatField()
    memo = models.CharField(max_length=255)
    ftid = models.CharField(max_length=255)

    def completeTransactionImport(self, accountObject):

        cashTransModelQuerySet = main.models.CashTransaction.objects.filter(account=accountObject, ftid=self.ftid)
        if(len(cashTransModelQuerySet) > 0):
            print("WARNING: transaction already exists. Not saving")
            return

        cashTransModel = main.models.CashTransaction()
        cashTransModel.account = accountObject
        cashTransModel.date = self.date
        cashTransModel.amount = self.amount
        cashTransModel.memo = self.memo
        cashTransModel.ftid = self.ftid
        cashTransModel.save()
