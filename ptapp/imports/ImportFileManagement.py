from ofxparse import OfxParser
from pathlib import Path
import json
from datetime import datetime, timezone, timedelta

from django.core.exceptions import ObjectDoesNotExist

from main.models import Accounts
from main.types import InvestmentTransactionTypes, InvestmentTransactionIncomeTypes
from .models import FileData, AccountData, CashAccountData, CashTransaction, InvestmentAccountData, InvestmentPosition, InvestmentTransaction
from .exceptions import FileImportException

#######################################################
# Class for managing file imports.
######################################################
class FileImporter:
    """ Class for managing file imports. It provides an entry point.
        Give it the file and it will select the approprate import routine and
        parse the file. It also manages writing that file to the temporary database.
    """

    # List of filetypes that we support
    FILETYPE_UNKNOWN = 0
    FILETYPE_QFX = 1 # QFX or OFX

    ACCOUNT_TYPE_BANK = 1

    #---------------------------------------------------------------------------#
    def __init__(self, filename, fileobj = None):
        """
        Initializes the class. Given the filename and information it will select
        the import routine.

        @param filename: string - the name of the file in question.
        @param fileobj: A file like object for reading. Django file uploads don't necessarily save the file to disk

        """
        self.fileData = None

        #How long the file should remain in the database in days
        self.fileExpiration = 30

        self.filename = filename
        self.fileObj = fileobj

        # First lets determine the type of file we are parsing.
        filetype = self.getFileType(filename)

        if(filetype == self. FILETYPE_UNKNOWN):
            raise FileImportException("Unknown Filetype")
        else:
            self.fileParser = OFXFile(fileobj = fileobj)

        self.fileHash = FileData.calculatefilehash(fileobj)

    #---------------------------------------------------------------------------#
    def getFileType(self, filename):
        """
        Determine what type of file this is.

        @param filename: string - the name of the file.
        @return the file type
        """

        extension = Path(filename).suffix
        if((extension.lower() == ".qfx") or (extension.lower() == ".ofx")):
            return self.FILETYPE_QFX
        else:
            return self.FILETYPE_UNKNOWN

    #--------------------------------------------------------------------------#
    def importFile(self):
        """
        Actually perform the import. This will check the database to see if the
        file already exists and if not. do the import.
        """

        recordsInDb = FileData.objects.filter(pk=self.fileHash)
        if(len(recordsInDb) == 0):
            self.__writeFileToDb()
        elif(len(recordsInDb) > 1):
            raise FileImportException("Duplicate records found!. Database integrity compromised. Please remedy this before continuing.")
        else:
            # There must already have been a file in the database. So just load it.
            self.fileData = recordsInDb[0]

    #--------------------------------------------------------------------------#
    def __writeFileToDb(self):
        """
        Take the parsed file and write it to the database. This is so we can come
        back to it when it is time for the user to confirm the match and any other Information
        """

        #Write the data about the file itself
        self.fileData = FileData()
        self.fileData.fileid = self.fileHash
        self.fileData.filename = self.filename
        self.fileData.expiration = datetime.now(timezone.utc) + timedelta(days=self.fileExpiration)
        self.fileData.save()

        # Call the file parser to read the contents of the file into the database.
        parsedData = self.fileParser.readInsertData(self.fileData)


    #--------------------------------------------------------------------------#
    @staticmethod
    def matchAccountWithExisting(account_id, institution_id):
        """
        Matching algorithm to match accounts in the file with accounts already in the database

        @param account_id - string - the account ide
        @param insitution_id - string - the institution id

        @return The database object or None if not matched
        """
        existingAccountsModel = Accounts.objects
        try:
            existingAccount = existingAccountsModel.get(account_id = account_id, institution_id = institution_id)
            return existingAccount
        except ObjectDoesNotExist:
            return None

################################################################################
# Parser class for QFX/OFX FILES
################################################################################
class OFXFile:
    """
    Object representing the data in an ofx file as well as functions for formatting and validating it for import
    """
    #-------------------------------------------------------------------------#
    def __init__(self, filename = None, fileobj = None):
        """
        @param filename - string - name of the ofx file to be imported
        @param fileobj - File Object - file object representing a particular file
        """

        if(filename != None):
            self.filename = filename

            with open(filename, 'rb') as fileobj:
                self.ofx = OfxParser.parse(fileobj)
        elif(fileobj != None):
            self.ofx = OfxParser.parse(fileobj)
        else:
            raise FileImportException("Must specify either a filename or a file object")

        self.accountData = list()

    #--------------------------------------------------------------------------#
    def mapAccountType(self, accountType):
        """
        Map the account type to the types in the Accounts model
        """
        if(accountType == 0):
            raise FileImportException("Unknown Account Type discovered in file!")
        elif(accountType == 1):
            return Accounts.CASH_TYPE
        elif(accountType == 2):
            raise FileImportException("Unsupported Account type CreditCard")
        elif(accountType == 3):
            return Accounts.STOCK_TYPE

    #--------------------------------------------------------------------------#
    def readInsertData(self, fileEntry):
        """ Import the data from an ofx file into a temporary table for confirmation"""

        # For now we will only allow one account to be present in the ofx file.
        # If more than one is found, we will throw an error and assess what it is
        #if(len(self.ofx.accounts) > 1):
        #    raise Exception("We did not expect to see more than one account in an OFX file!")

            #Write account information
        for account in self.ofx.accounts:
            accountType = self.mapAccountType(account.type)

            if(accountType == Accounts.CASH_TYPE ):
                model = CashAccountData()
            elif(accountType == Accounts.STOCK_TYPE):
                model = InvestmentAccountData()
            else:
                raise NotImplementedError("Non Cashtype account detected. We don't handle that yet. ")

            model.file = fileEntry
            model.type = accountType
            model.account_id = account.account_id
            model.routing_number = account.routing_number
            model.institution_name = account.institution.organization
            model.institution_id = account.institution.fid
            # Some QFXs don't define the currency, so we use the default.
            if(account.curdef is not None):
                model.currency_symbol = account.curdef

            #Match it with an existing account
            match = FileImporter.matchAccountWithExisting(model.account_id, model.institution_id)
            if(match == None):
                print("Model not matched in import")
                model.matched = False
            else:
                print("Model matched in import")
                model.matched = True
                model.matched_account_id = match

            # Start saving statement information like balance and positions.
            # If the account type is a cash one, add the fields specific to cash accounts
            if(accountType == Accounts.CASH_TYPE):
                model.balance = account.statement.balance
                model.balance_date = account.statement.balance_date
            # If it's a stock type, add the fields specific to stock types
            elif(accountType == Accounts.STOCK_TYPE):
                model.position_date = account.statement.end_date

                # get a list of securities referenced in this document
                self.security_list = self.getStatementSecurityList(self.ofx)

            else:
                raise FileImportException("Unsupported account type at transaction import")

            model.save()

            # Start saving transactions and positions
            if(accountType == Accounts.CASH_TYPE):
                self.parseCashTransactions(account, model)
            elif(accountType == Accounts.STOCK_TYPE):
                self.parseStockPositionData(account, model)
                self.parseInvestmentTransactionData(account, model)
            else:
                raise NotImplementedError("Non cash type account detected. We don't handle that yet")

    #--------------------------------------------------------------------------#
    def parseCashTransactions(self, ofxAccount, accountDBObject):
        stmt = ofxAccount.statement
        for tran in stmt.transactions:
            transactionModel = CashTransaction()
            transactionModel.date = tran.date
            transactionModel.amount = tran.amount
            transactionModel.ftid = tran.id
            transactionModel.memo = tran.memo
            transactionModel.account = accountDBObject
            transactionModel.save()

    #--------------------------------------------------------------------------#
    def getStatementSecurityList(self, ofxObject):
        """ Investment account statements have a security_list entry that lists basic
        information about securities referenced in the document. We should parse
        this and return it as a library of objects for reference when parsing
        transactions and positions

        We create a dictionary with keys using the ticker symbol (upper case) and
        the CUSIP id. There won't be too many, so I think it will be ok to have
        each security appear twice.
        """
        security_list = dict()

        for s in ofxObject.security_list:
            print(dir(s))
            security_list[s.uniqueid] = {
                'uniqueId': s.uniqueid,
                'ticker': s.ticker.upper(),
                'name': s.name,
                'memo': s.memo
            }
            security_list[s.ticker.upper()] = security_list[s.uniqueid]
        return security_list

    #--------------------------------------------------------------------------#
    def parseStockPositionData(self, ofxAccount, accountDBObject):
        positionList = ofxAccount.statement.positions

        for p in positionList:
            positionModel = InvestmentPosition()
            positionModel.account = accountDBObject
            positionModel.ticker = self.security_list[p.security]['ticker']
            positionModel.CUSIP = p.security
            positionModel.units = p.units
            positionModel.unit_price = p.unit_price
            positionModel.save()

    #--------------------------------------------------------------------------#
    def parseInvestmentTransactionData(self, ofxAccount, accountDBObject):
        #lets set up some mappings to types
        incomeTypeList = {
            "CGLONG": InvestmentTransactionIncomeTypes.CGLONG,
            "CGSHORT": InvestmentTransactionIncomeTypes.CGSHORT,
            "DIV": InvestmentTransactionIncomeTypes.DIV,
            "INTEREST": InvestmentTransactionIncomeTypes.INTEREST,
            "MISC": InvestmentTransactionIncomeTypes.MISC
        }

        transactionTypeList = {
            "buydebt": InvestmentTransactionTypes.BUY_DEBT,
            "buymf": InvestmentTransactionTypes.BUY_MF,
            "buyopt": InvestmentTransactionTypes.BUY_OPT,
            "buyother": InvestmentTransactionTypes.BUY_OTHER,
            "buystock": InvestmentTransactionTypes.BUY_STOCK,
            "closureopt": InvestmentTransactionTypes.CLOSURE_OPT,
            "income": InvestmentTransactionTypes.INCOME,
            "invexpense": InvestmentTransactionTypes.INV_EXPENSE,
            "jrnlfund": InvestmentTransactionTypes.JRNL_FUND,
            "jrnlsec": InvestmentTransactionTypes.JRNL_SEC,
            "margininterest": InvestmentTransactionTypes.MARGIN_INTEREST,
            "reinvest": InvestmentTransactionTypes.REINVEST,
            "retofcap": InvestmentTransactionTypes.RET_OF_CAP,
            "selldebt": InvestmentTransactionTypes.SELL_DEBT,
            "sellmf": InvestmentTransactionTypes.SELL_MF,
            "sellopt": InvestmentTransactionTypes.SELL_OPT,
            "sellother": InvestmentTransactionTypes.SELL_OTHER,
            "sellstock": InvestmentTransactionTypes.SELL_STOCK,
            "split": InvestmentTransactionTypes.SPLIT,
            "transfer": InvestmentTransactionTypes.TRANSFER
        }

        transactionList = ofxAccount.statement.transactions

        for t in transactionList:
            print(vars(t))
            transactionModel = InvestmentTransaction()
            transactionModel.account = accountDBObject

            transactionModel.ftid = t.id

            if(t.type.lower() not in transactionTypeList.keys()):
                raise FileImportException("Unknown investment transaction type.")
            elif(t.type.lower() == "transfer"): #I don't know what the tferaction variable does, so if we see a transfer, stop it so i can see. Take this out when i figure it out.
                raise FileImportException("Transfer type detected, now is the time to figure out the tferaction variable.")
            else:
                transactionModel.type = transactionTypeList[t.type.lower()]

            transactionModel.tradeDate = t.tradeDate

            #If there was no settle date, we'll say it settled on the same day as the trade
            if(t.settleDate is None):
                transactionModel.settleDate = t.tradeDate
            else:
                transactionalModel.settleDate = t.settleDate

            transactionModel.memo = t.memo
            transactionModel.CUSIP = t.security
            transactionModel.ticker = self.security_list[t.security]['ticker']

            if(t.income_type is ""):
                transactionModel.income_type = InvestmentTransactionIncomeTypes.NOTINCOME
            elif (t.income_type.upper() not in incomeTypeList.keys()):
                raise FileImportException("Unknown investment transaction income type: %s" % t.income_type.upper())
            else:
                transactionModel.income_type = incomeTypeList[t.income_type.upper()]

            transactionModel.units = t.units
            transactionModel.unit_price = t.unit_price

            if(hasattr(t, 'comission')):
                transactionModel.comission = t.comission

            transactionModel.fees = t.fees
            #We keep the total instead of calculating it, because some transactions only use that field.
            transactionModel.total = t.total
            transactionModel.save()
