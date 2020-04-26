from ofxparse import OfxParser
from pathlib import Path
import json
from datetime import datetime, timezone, timedelta

from django.core.exceptions import ObjectDoesNotExist

from .models import FileImport_FileData, FileImport_AccountData, Accounts

#######################################################
# Class for managing file imports.
######################################################
class FileImporter:
    """ Class for managing file imports. It provides an entry point.
        Give it the file and it will select the approprate import routine and
        parse the file. It also manages writing that file to the temporary database.

        Format of parsedData object:
        [
            {
                "account_id": "1234",
                "routing_number": "131345648",
                "institution_name": "The Bank of Awesome",
                "institution_id": "1234",
                "account_type": "cash",
                "currency_symbol": "USD"
            },
            ...
            
        ]

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
            raise Exception("Unknown Filetype")
        else:
            self.fileParser = OFXFile(fileobj = fileobj)

        self.fileHash = FileImport_FileData.calculatefilehash(fileobj)

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

        recordsInDb = FileImport_FileData.objects.filter(pk=self.fileHash)
        if(len(recordsInDb) == 0):
            self.__writeFileToDb()
        elif(len(recordsInDb) > 1):
            raise Exception("Duplicate records found!. Please remedy this before continuing.")
        else:
            # There must already have been a file in the database. So just load it.
            self.fileData = recordsInDb[0]

    #--------------------------------------------------------------------------#
    def __parseFile(self):
        return self.fileParser.parseFileData()

    #--------------------------------------------------------------------------#
    def __writeFileToDb(self):
        """
        Take the parsed file and write it to the database. This is so we can come
        back to it when it is time for the user to confirm the match and any other Information
        """
        parsedData = self.__parseFile()

        #Write the data about the file itself
        self.fileData = FileImport_FileData()
        self.fileData.fileid = self.fileHash
        self.fileData.filename = self.filename
        self.fileData.expiration = datetime.now(timezone.utc) + timedelta(days=self.fileExpiration)
        self.fileData.save()

        #Write account information
        for account in parsedData:
            model = FileImport_AccountData()
            model.file = self.fileData
            model.account_id = account['account_id']
            model.routing_number = account['routing_number']
            model.institution_name = account['institution_name']
            model.institution_id = account['institution_id']
            model.currency_symbol = account['currency_symbol']
            model.balance = 0.00
            model.balance_date = datetime.now()

            #Match it with an existing account
            match = self.matchAccountWithExisting(model.account_id, model.institution_id)
            if(match == None):
                model.matched = False
            else:
                model.matched = True
                model.matched_account_id = match
            model.save()

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
            raise Exception("Must specify either a filename or a file object")

        self.accountData = list()

    #--------------------------------------------------------------------------#
    def mapAccountType(self, accountType):
        """
        Map the account type to the types in the Accounts model
        """
        if(accountType == 0):
            raise Exception("Unknown Account Type!")
        elif(accountType == 1):
            return Accounts.CASH_TYPE
        elif(accountType == 2):
            raise Exception("Unsupported Account type CreditCard")
        elif(accountType == 3):
            return Accounts.STOCK_TYPE

    #--------------------------------------------------------------------------#
    def parseFileData(self):
        """ Import the data from an ofx file into a temporary table for confirmation"""

        # For now we will only allow one account to be present in the ofx file.
        # If more than one is found, we will throw an error and assess what it is
        #if(len(self.ofx.accounts) > 1):
        #    raise Exception("We did not expect to see more than one account in an OFX file!")

        for account in self.ofx.accounts:

            self.accountData.append( {
                'account_id': account.account_id,
                'routing_number': account.routing_number,
                'institution_name': account.institution.organization,
                'institution_id': account.institution.fid,
                'account_type': self.mapAccountType(account.type),
                'currency_symbol': account.curdef
            })

        return self.accountData