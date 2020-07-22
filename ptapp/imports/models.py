from django.db import models, transaction
import hashlib

import main
from main.models import CashAccounts, Accounts
from main.types import InvestmentTransactionTypes, InvestmentTransactionIncomeTypes, AccountTypes

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
                #Get the correct subtype since what was returned was the generic account type
                fileAccount = a.getSubclass()
                #If there was a matched account, then we get it.
                if(fileAccount.matched):
                    mainAccountModel = fileAccount.matched_account_id.getSubclass()
                else:
                    #If this is a new account, the importing account model creates a new main account model.
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
    type = models.IntegerField(choices = AccountTypes.choices(), default=AccountTypes.BANK_TYPE)
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
        if(self.type == AccountTypes.BANK_TYPE):
            return self.cashaccountdata
        elif(self.type == AccountTypes.INVESTMENT_TYPE):
            return self.investmentaccountdata
        else:
            raise NotImplementedError("Tried to get an unknown account type %s" % self.type)

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
        destinationAccount.save()

################################################################################
# CashAccountData - Temporary Specific table for cash accounts
################################################################################
class CashAccountData(AccountData):
    balance = models.DecimalField(max_digits=13, decimal_places=2)
    balance_date = models.DateTimeField()

    #--------------------------------------------------------------------------#
    def getNewCorrespondingModel(self):
        """Return a new empty model of the correct type to be filled"""
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
            # The assumption is that a transaction won't change over time.
            # If we got it in one import, it won't be different if it shows up in the next.
            print("WARNING: cash transaction already exists. Not saving")
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

    #--------------------------------------------------------------------------#
    def getNewCorrespondingModel(self):
        """Returns a new empty model of the correct type to be filled."""
        return main.models.InvestmentAccounts()

    #--------------------------------------------------------------------------#
    def completeAccountImport(self, destinationAccount):
        #Update the generic details
        super().completeAccountImport(destinationAccount)

        print(destinationAccount.position_date)
        # Update the position info for this account
        # But only if the positiion date is more recent than the stored date.
        if((destinationAccount.position_date is None) or (destinationAccount.position_date < self.position_date)):
            destinationAccount.position_date = self.position_date
            for p in self.positions.all():
                p.completePositionImport(destinationAccount)

        for t in self.transactions.all():
            t.completeTransactionImport(destinationAccount)

        destinationAccount.save()


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

    #--------------------------------------------------------------------------#
    def completePositionImport(self, destinationAccount):
        positionModelQuerySet = main.models.InvestmentPosition.objects.filter(account=destinationAccount, ticker=self.ticker)
        numPositionsReturned = len(positionModelQuerySet)
        if(numPositionsReturned == 0):
            positionModel = main.models.InvestmentPosition()
            positionModel.account = destinationAccount
            positionModel.ticker = self.ticker
            positionModel.CUSIP = self.CUSIP
        elif(numPositionsReturned == 1):
            positionModel = positionModelQuerySet[0]

        positionModel.units = self.units
        positionModel.unit_price = self.unit_price
        positionModel.save()

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

    #--------------------------------------------------------------------------#
    def completeTransactionImport(self, destinationAccount):
        investmentTransModelQuerySet = main.models.InvestmentTransaction.objects.filter(account=destinationAccount, ftid=self.ftid)
        if(len(investmentTransModelQuerySet) > 0):
            # The assumption is that a transaction won't change over time.
            # If we got it in one import, it won't be different if it shows up in the next.
            print("WARNING: investment transaction already exists. Not Saving")
            return

        invTransModel = main.models.InvestmentTransaction()
        invTransModel.account = destinationAccount
        invTransModel.ftid = self.ftid
        invTransModel.type = self.type
        invTransModel.tradeDate = self.tradeDate
        invTransModel.settleDate = self.settleDate
        invTransModel.memo = self.memo
        invTransModel.CUSIP = self.CUSIP
        invTransModel.ticker = self.ticker
        invTransModel.income_type = self.income_type
        invTransModel.units = self.units
        invTransModel.unit_price = self.unit_price
        invTransModel.comission = self.comission
        invTransModel.fees = self.fees
        invTransModel.total = self.total
        invTransModel.save()
