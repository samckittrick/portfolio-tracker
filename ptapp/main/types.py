from enum import IntEnum

################################################################################
# The different types of accounts we can have
################################################################################
class AccountTypes(IntEnum):
    # Cash Bank Accounts
    BANK_TYPE = 1
    # Investment Accounts
    INVESTMENT_TYPE = 2

    #----------------------------------------------------------------------#
    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


###########################################################################
# The different types of transactions and the string that represents them
###########################################################################
class InvestmentTransactionTypes(IntEnum):
    # Buy a debt security
    BUY_DEBT = 1
    # Buy a Mutual fund
    BUY_MF = 2
    # Buy an Option
    BUY_OPT = 3
    # Buy something else
    BUY_OTHER = 4
    # Buy a Stock
    BUY_STOCK = 5
    # Close a position for an option
    CLOSURE_OPT = 6
    # Investment income is realized as cash into the investment account
    INCOME = 7
    # Investment expenses associated with a specific security
    INV_EXPENSE = 8
    # Journal a fund from one sub account to another
    # Link to an explanation of Norberts Gambit, which uses journalling
    # https://wealthsavvy.ca/norberts-gambit-questrade/
    JRNL_FUND = 9
    # Journal a security from one sub account to another
    JRNL_SEC = 10
    # Interest on loans for securities bought on margin
    MARGIN_INTEREST = 11
    # Reinvestment of income
    REINVEST = 12
    # Return of Capital
    RET_OF_CAP = 13
    # Sell a debt security
    SELL_DEBT = 14
    # Sell a Mutual Fund
    SELL_MF = 15
    # Sell an option
    SELL_OPT = 16
    # Sell some other type of security
    SELL_OTHER = 17
    # Sell a stock
    SELL_STOCK = 18
    # Stock or mutual fund split
    SPLIT = 19
    # Transfer of holdings in and out of investment account.
    TRANSFER = 20

    #----------------------------------------------------------------------#
    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

    #----------------------------------------------------------------------#
    @classmethod
    def mapTypeToName(cls, type):
        typeMappings = {
            cls.BUY_DEBT: 'Buy Debt Security',
            cls.BUY_MF: 'Buy Mutual Fund',
            cls.BUY_OPT: 'Buy Option',
            cls.BUY_OTHER: 'Buy Other Security',
            cls.BUY_STOCK: 'Buy Stock',
            cls.CLOSURE_OPT: 'Close Option',
            cls.INCOME: 'Income',
            cls.INV_EXPENSE: 'Investment Expense',
            cls.JRNL_FUND: 'Journal Fund',
            cls.JRNL_SEC: 'Journal Security',
            cls.MARGIN_INTEREST: 'Margin Interest',
            cls.REINVEST: 'Reinvest',
            cls.RET_OF_CAP: 'Return of Capital',
            cls.SELL_DEBT: 'Sell Debt Security',
            cls.SELL_MF: 'Sell Mutual Fund',
            cls.SELL_OPT: 'Sell Option',
            cls.SELL_OTHER: 'Sell Other Security',
            cls.SELL_STOCK: 'Sell Stock',
            cls.SPLIT: 'Split Security',
            cls.TRANSFER: 'Transfer'
        }

        return typeMappings[type]

############################################################################
# Different Types of income for an investment transaction
############################################################################
class InvestmentTransactionIncomeTypes(IntEnum):
    # No Income type. Might not be income
    NOTINCOME = 0
    # Long term capital gains
    CGLONG = 1
    # Short Term Capital Gains
    CGSHORT = 2
    # Dividend
    DIV = 3
    # INTEREST
    INTEREST = 4
    # Misc Income
    MISC = 5

    #---------------------------------------------------------------------#
    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
