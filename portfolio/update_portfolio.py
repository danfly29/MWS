import sqlite3

class Portfolio:
    '''This is a class to create a portfolio table and update the contents of
    such portfolio. The initiate method is meant to be used once and the update
    method is meant to be used from there after. Both of this methods feed of
    the rest of the methods.'''

    def get_price(self):
        pass

    def get_name(self):
        pass

    def get_ammount(self):
        pass

    def get_type(self):
        pass

    def equity_and_proportion(self):
        pass

    def initiate(self):
        str = input('Do you wish to insert a ticker in the portfolio table (Y/N):')
        self.cont_q = str
        while self.cont_q == 'Y':
            self.entry_name = self.get_name()
            self.entry_ammount = self.get_ammount()
            self.entry_type = self.get_type()
            self.entry_price = self.get_price()
            self.entry_equity = self.equity_and_proportion()
            str = input('Do you wish to insert a ticker in the portfolio table (Y/N):')
            self.cont_q = str
