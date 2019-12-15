import re #For regular expression

from bs4 import BeautifulSoup #For making html file prety

from functions import *




class StockTicker:
    def load(self,i):
        self.name = i
        self.html = html_retrieve(i)
        self.industry = industry(self.html)
        self.pe = pe_regex(self.html)
        self.pb = pbook_regex(self.html)
        self.pcf = pcf_regex(self.html)
        self.ev_ebitda = ev_ebitda_regex(self.html)
        self.current = current_ratio_regex(self.html)
        self.roe = roe_regex(self.html)
        self.total_ratio = tdebt_to_tequity_regex(self.html)
        self.date = day()


n = StockTicker()
n.load("MU")
