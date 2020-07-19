from django.db import models, transaction
import hashlib

import main
from main.models import CashAccounts, Accounts
from main.types import InvestmentTransactionTypes, InvestmentTransactionIncomeTypes

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
                fileAccount = a.getSubclass()
                if(fileAccount.matched):
                    mainAccountModel = fileAccount.matched_account_id
                else:
                    mainAccountModel = fileAccount.getNewCorrespondingModel()
                fileAccount.completeAccountImport(mainAccountModel)


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
    currency_symbol = models.CharField(max_length=3, default="USD")
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
    def completeAccountImport(self, destinationAccount):
        """
        Save the fields that are common to all accounts to the given Accounts object
        """
        if(self.friendlyName != ""):
            destinationAccount.name = self.friendlyName
        else:
            destinationAccount.name = self.account_id
        destinationAccount.account_id = self.account_id
        destinationAccount.institution_name = self.institution_name
        destinationAccount.institution_id = self.institution_id
        destinationAccount.routing_number = self.routing_number
        destinationAccount.currency_symbol = self.currency_symbol
        destinationAccount.type = self.type

################################################################################
# CashAccountData - Temporary Specific table for cash accounts
################################################################################
class CashAccountData(AccountData):
    balance = models.DecimalField(max_digits=13, decimal_places=2)
    balance_date = models.DateTimeField()

    #--------------------------------------------------------------------------#
    def getNewCorrespondingModel(self):
        """Return a new empty model to be filled"""
        return main.models.CashAccounts()

    #--------------------------------------------------------------------------#
    def completeAccountImport(self, destinationAccount):
        #Update the generic details.
        super().completeAccountImport(destinationAccount)

        # Update balance of matched or unmatched account.
        # But only if the statement date is more recent than the stored date
        if((destinationAccount.balance_date is None) or (destinationAccount.balance_date < self.balance_date)):
            destinationAccount.balance = self.balance
            destinationAccount.balance_date = self.balance_date

        destinationAccount.save()

        # Whether we matched or not, we also need to import transaction
        for t in self.transactions.all():
            t.completeTransactionImport(destinationAccount)

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

################################################################################
# InvestmentAccount - Subclass for investment accounts specifically
################################################################################
class InvestmentAccountData(AccountData):
    # We need to know when the
    position_date = models.DateTimeField()

################################################################################
# InvestmentPositions - List of security positions for a specific account.
###############################################################################
class InvestmentPosition(models.Model):

    account = models.ForeignKey(InvestmentAccountData, on_delete=models.CASCADE, related_name="positions")

    ticker = models.CharField(max_length=8)
    CUSIP = models.CharField(max_length=16)
    # Depending on the broker, it's possible to hold partial shares. So we use a float.
    units = models.FloatField()
    unit_price = models.FloatField()

################################################################################
# InvestmentTransaction
################################################################################
class InvestmentTransaction(models.Model):
    account = models.ForeignKey(InvestmentAccountData, on_delete=models.CASCADE, related_name="transactions")
    ftid = models.CharField(max_length=255)

    type = models.IntegerField(choices=InvestmentTransactionTypes.choices(),
                                default = InvestmentTransactionTypes.BUY_OTHER
                               )
    tradeDate = models.DateTimeField()
    settleDate = models.DateTimeField()
    memo = models.CharField(max_length=255)
    CUSIP = models.CharField(max_length=16)
    ticker = models.CharField(max_length=8)
    income_type = models.IntegerField(choices = InvestmentTransactionIncomeTypes.choices())
    # Depending on the broker, it's possible to hold partial shares. So we use a float
    units = models.FloatField(default = 0)
    unit_price = models.FloatField(default =0)
    comission = models.FloatField(default = 0)
    fees = models.FloatField(default = 0)
    total = models.FloatField(default = 0)
