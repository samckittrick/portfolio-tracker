#
# StockDB Object controls access to the relational database for storing stock information
#
import mysql.connector

class StockDB:
    """ Object for controlling access to the relational database for storing stock information"""

    #--------------------------------------------------------------------
    def __init__(self, db_host, db_port, db_name, db_user, db_password):
        self.hostname = db_host
        self.port = db_port
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password

    #-----------------------------------------------------------------------
    def __getConnection(self):
        """ Get a database connection """
        return mysql.connector.connect(user=self.db_user, password=self.db_password, host=self.hostname, port=self.port, database=self.db_name)

    #---------------------------------------------------------------------
    def getTrackedStocks(self):
        """ Get a list of stocks being tracked by portfolio tracker"""

        query = "select `symbol` from `symbols`"
        conn = self.__getConnection()
        cursor = conn.cursor()

        cursor.execute(query)

        symbolList = list()
        for symbol in cursor:
            #Each row is a tuple, but we only have one column, so just append that first column
            symbolList.append(symbol[0])

        return symbolList
