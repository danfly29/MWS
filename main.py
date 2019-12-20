import re #For regular expression
import sqlite3
from bs4 import BeautifulSoup #For making html file prety
import time #for pauses


from functions import *

class Manager():

    def read_list(self):
        hand = open('list.txt','r')

    def initiate_db(self):
        conn = sqlite3.connect('mws.sqlite')
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS SP500_Data (id INTEGER PRIMARY KEY, Date TEXT,
         Symbol TEXT UNIQUE, PE  REAL, PS  REAL, PB  REAL, PCF  REAL,
         EVEBITDA REAL, Current  REAL, ROE REAL, DE  REAL, Description TEXT)''')

    def commit(self):
        conn = sqlite3.connect('mws.sqlite')
        cur = conn.cursor()
        conn.commit()

    def update(self):
        cur.execute('''UPDATE SP500_Data SET Date = ?,
            PE = ?, PCF = ?, PB = ?,  PS = ?,
            EVEBITDA = ?, Current = ?, ROE = ?, DE = ?, Description = ?
            WHERE Symbol = ?
             ''',(self.date,self.pe,self.pcf,self.pb,self.ps,self.ev_ebitda,self.current,self.roe,self.total_ratio, self.industry, self.name))

    def save(self,ticker):
        conn = sqlite3.connect('mws.sqlite')
        cur = conn.cursor()
        cur.execute('''INSERT INTO SP500_Data (Date, Symbol,
            PE, PCF, PB, PS, EVEBITDA, Current, ROE, DE, Description
            )
            VALUES (?,?,?,?,?,?,?,?,?,?,?)
            ''',(ticker.date, ticker.name, ticker.pe, ticker.pcf, ticker.pb, ticker.ps, ticker.ev_ebitda, ticker.current, ticker.roe, ticker.total_ratio, ticker.industry))
        conn = sqlite3.connect('mws.sqlite')
        cur = conn.cursor()
        conn.commit()
        print('Saved ', ticker.name)

    def printer(self,ticker):
        print(ticker.date,ticker.pe,ticker.pcf,ticker.pb,ticker.ps,ticker.ev_ebitda,ticker.current,ticker.roe,ticker.total_ratio, ticker.industry, ticker.name)


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
limit = 50

hand = open('list.txt','r')
iteration= 0
for line in hand:
    line = line.rstrip()
    ticker = StockTicker()
    ticker.scrape(line)
    manager.save(ticker)

    iteration += 1
    if iteration == limit:
        #manager.commit()
        break
    if iteration%4 == 0 and iteration != 0:
        print('===================Taking a Nap=====================')
        #manager.commit()
        time.sleep(30)
