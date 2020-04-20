from ofxparse import OfxParser

class OFXFile:
    """
    Object representing the data in an ofx file as well as functions for formatting it for import
    """

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

        self.parsedData = list()
        self.__parseFileData()

    def __parseFileData(self):
        """ Import the data from an ofx file into a temporary table for confirmation"""

        for account in self.ofx.accounts:
            accountData = {
                'account_id': account.account_id,
                'routing_number': account.routing_number,
                'institution_name': account.institution.organization,
                'institution_id': account.institution.fid,
                'account_type': type,
                'currency_symbol': account.curdef
            }
            self.parsedData.append(accountData)
