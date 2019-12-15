import re #For regular expression
import sqlite3
from bs4 import BeautifulSoup #For making html file prety

from functions import *

class Manager():
    def read_list():
        hand = open('list.txt','r')

    def initiate_db(self):
        conn = sqlite3.connect('mws.sqlite')
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS SP500_Data (id INTEGER PRIMARY KEY, Date TEXT,
         Symbol TEXT UNIQUE, PE  REAL, PS  REAL, PB  REAL, PCF  REAL,
         EVEBITDA REAL, Current  REAL, ROE REAL, DE  REAL, Description TEXT)''')

    def update(self):
        cur.execute('''UPDATE SP500_Data2 SET Date = ?,
            PE = ?, PCF = ?, PB = ?,  PS = ?,
            EVEBITDA = ?, Current = ?, ROE = ?, DE = ?, Description = ?
            WHERE Symbol = ?
             ''',(self.date,self.pe,self.pcf,self.pb,self.ps,self.ev_ebitda,self.current,self.roe,self.total_ratio, self.industry, self.name))

    def printer(self,ticker,i):
        print(ticker.date,ticker.pe,ticker.pcf,ticker.pb,ticker.ps,ticker.ev_ebitda,ticker.current,ticker.roe,ticker.total_ratio, ticker.industry, ticker.name,i)


class StockTicker:
    def scrape(self,i):
        self.name = i
        self.html = html_retrieve(i)
        self.industry = industry(self.html)
        self.pe = pe_regex(self.html)
        self.pb = pbook_regex(self.html)
        self.pcf = pcf_regex(self.html)
        self.ps = ps_regex(self.html)
        self.ev_ebitda = ev_ebitda_regex(self.html)
        self.current = current_ratio_regex(self.html)
        self.roe = roe_regex(self.html)
        self.total_ratio = tdebt_to_tequity_regex(self.html)
        self.date = day()

manager = Manager()
manager.initiate_db()

hand = open('list.txt','r')
n = 0
for line in hand:
    line = line.rstrip()
    ticker = StockTicker()
    ticker.scrape(line)
    manager.printer(ticker,n)

    n+=1
    if n == 2:
        #manager.commit()
        break
