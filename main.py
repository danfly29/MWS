import re #For regular expression
import sqlite3
from bs4 import BeautifulSoup #For making html file prety
import time #for pauses


from functions import *

class Manager:


    def read_names_db(self):
        conn =sqlite3.connect('mws.sqlite')
        cur = conn.cursor()
        cur.execute('SELECT Symbol FROM SP500_Data')
        list = cur.fetchall()
        nlist=[]
        for i in list:
            nlist.append(i[0])
        return(nlist)

    def initiate_db(self):
        conn = sqlite3.connect('mws.sqlite')
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS SP500_Data (id INTEGER PRIMARY KEY, Date TEXT,
         Symbol TEXT UNIQUE, PE  REAL, PS  REAL, PB  REAL, PCF  REAL,
         EVEBITDA REAL, Current  REAL, ROE REAL, DE  REAL, Description TEXT)''')
        self.list = self.read_names_db()

    def commit(self):
        conn = sqlite3.connect('mws.sqlite')
        conn.commit()

    def update(self,ticker):
        conn = sqlite3.connect('mws.sqlite')
        cur = conn.cursor()
        cur.execute('''UPDATE SP500_Data SET Date = ?,
            PE = ?, PCF = ?, PB = ?,  PS = ?,
            EVEBITDA = ?, Current = ?, ROE = ?, DE = ?, Description = ?
            WHERE Symbol = ?
             ''',(ticker.date, ticker.name, ticker.pe, ticker.pcf, ticker.pb, ticker.ps, ticker.ev_ebitda, ticker.current, ticker.roe, ticker.total_ratio, ticker.industry))
        conn.commit()
        print('Saved ', ticker.name)

    def save(self,ticker):
        conn = sqlite3.connect('mws.sqlite')
        cur = conn.cursor()
        cur.execute('''INSERT INTO SP500_Data (Date, Symbol,
            PE, PCF, PB, PS, EVEBITDA, Current, ROE, DE, Description
            )
            VALUES (?,?,?,?,?,?,?,?,?,?,?)
            ''',(ticker.date, ticker.name, ticker.pe, ticker.pcf, ticker.pb, ticker.ps, ticker.ev_ebitda, ticker.current, ticker.roe, ticker.total_ratio, ticker.industry))
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
manager.list
limit = 250

hand = open('list.txt','r')
iteration= 0
for line in hand:
    print(line)
    line = line.rstrip()
    if line in manager.list:
        continue #Could do something once database is filled and need to decide between
        #updates, new entries or both
        #manager.update(ticker)
    else:
        ticker = StockTicker()
        ticker.scrape(line)
        manager.save(ticker)

    iteration += 1
    if iteration == limit:
        manager.commit()
        break
    if iteration%4 == 0 and iteration != 0:
        print('===================Taking a Nap=====================')
        #manager.commit()
        time.sleep(30)
