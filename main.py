import re #For regular expression

from bs4 import BeautifulSoup #For making html file prety

from functions import html_retrieve, industry, pe_regex




class StockTicker:
    def load(self,i):
        self.name = i
        self.html = html_retrieve(i)
        self.industry = industry(self.html)
        self.pe = pe_regex(self.html)


n = StockTicker()
n.load("MU")
