import sqlite3
from functions import *

class Manager:
    def interface(self):
        print('Wellcome to your fundamentals screener\n')
        self.list_in_db = self.read_names_for_update()
        scrape_str = input('Will you be scraping data of the web(y/n):')
        self.scrape_q = scrape_str.capitalize()
        if self.scrape_q == 'Y':
            list_str = input('Will you be using a self-made list(y/n):')
            self.list_q = list_str.capitalize()
            if self.list_q == 'Y':
                list_name = input('Type the name of your list-file: \n')
                self.list_name = list_name
            if self.list_q == 'N':
                print('Performing updates')
            try:
                limit = input('How many ticker will you be scraping:')
                self.limit = int(limit)
            except:
                print('This is awkard, was that a number?')
        if self.scrape_q == 'N':
            value_type = input('Will you be looking for under or over valued looking instruments(u/o):')
            self.value_type = value_type.capitalize()
            if self.value_type == 'U':
                self.value_type_int = 1
                self.undervalued_screener_setup()
            if self.value_type == 'O':
                self.value_type_int = -1
        self.screener_result = []

        print('Processing\n')

    def read_names_for_update(self):
        conn =sqlite3.connect('mws.sqlite')
        cur = conn.cursor()
        cur.execute('SELECT Symbol FROM SP500_Data ORDER BY Date')
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
             ''',(ticker.date, ticker.pe, ticker.pcf, ticker.pb, ticker.ps, ticker.ev_ebitda, ticker.current, ticker.roe, ticker.total_ratio, ticker.industry, ticker.name))
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
        print('Name: ', ticker.name)
        print('----------------------------------------------------')
        print('Last update:', ticker.date)
        print('Price to Earnings: ', ticker.pe)
        print('Price to Sales: ', ticker.ps)
        print('Price to Cash Flow:', ticker.pcf)
        print('Price to Book Value:', ticker.pb)
        print('EV/EBITDA:', ticker.ev_ebitda)
        print('CurrentRatio:',ticker.current)
        print('Return On Equity:',ticker.roe)
        print('Total Debt to Total Equity:', ticker.total_ratio)
        print('Description:',ticker.industry)

    def undervalued_screener_setup(self):
        try:
            self.PriceToEarnings = float(input('Enter the maximum Price to Earnings Ratio\n  '))
        except:
            self.PriceToEarnings = 18

        try:
            self.PriceToSales = float(input('Enter the maximum Price to Sales Ratio\n  '))
        except:
            self.PriceToSales = 2.33

        try:
            self.PriceToBook = float(input('Enter the maximum Price to Book\n  '))
        except:
            self.PriceToBook = 2.86

        try:
            self.PriceToCashFlow = float(input('Enter the maximum Price to Cash Flow\n  '))
        except:
            self.PriceToCashFlow = 12.6

        try:
            self.EVtoEBITDA = float(input('Enter the maximum Enterprise Value to EBITDA\n  '))
        except:
            self.EVtoEBITDA = 10

        try:
            self.CurrentRatio = float(input('Enter the minimum current Ratio\n  '))
        except:
            self.CurrentRatio = 1.2

        try:
            self.ROE =  float(input('Enter the minimum Return On Equity\n  '))
        except:
            self.ROE = 15

        try:
            self.TotalDebToTotalEquity = float(input('Enter the maximum Total Debt to Total Equity\n  '))
        except:
            self.TotalDebToTotalEquity = 50

    def screener(self,ticker):
        numberofnulls = 8
        if ticker.pe != None:
            if ticker.pe*self.value_type_int > self.PriceToEarnings*self.value_type_int:
                return
            numberofnulls -= 1
        if ticker.ps != None:
            if ticker.ps*self.value_type_int > self.PriceToSales*self.value_type_int:
                return
            numberofnulls -= 1
        if ticker.pb != None:
            if ticker.pb*self.value_type_int > self.PriceToBook*self.value_type_int:
                return
            numberofnulls -= 1
        if ticker.pcf != None:
            if ticker.pcf*self.value_type_int > self.PriceToCashFlow*self.value_type_int:
                return
            numberofnulls -= 1
        if ticker.ev_ebitda != None:
            if ticker.ev_ebitda*self.value_type_int > self.EVtoEBITDA*self.value_type_int:
                return
            numberofnulls -= 1
        if ticker.current != None:
            if ticker.current*self.value_type_int > self.CurrentRatio*self.value_type_int:
                return
            numberofnulls -= 1
        if ticker.roe != None:
            if ticker.roe*self.value_type_int > self.ROE*self.value_type_int:
                return
            numberofnulls -= 1
        if ticker.total_ratio != None:
            if ticker.total_ratio*self.value_type_int > self.TotalDebToTotalEquity*self.value_type_int:
                return
            numberofnulls -= 1
        if numberofnulls > 3:
            return
        self.screener_result.append(ticker.name)


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

    def reload(self,i):
        conn = sqlite3.connect('mws.sqlite')
        cur = conn.cursor()
        self.name = i
        cur.execute('SELECT * FROM SP500_Data WHERE Symbol = ?',(self.name,))
        ilist = cur.fetchall()
        self.date = ilist[0][1]
        self.pe = ilist[0][3]
        self.ps = ilist[0][4]
        self.pb = ilist[0][5]
        self.pcf = ilist[0][6]
        self.ev_ebitda = ilist[0][7]
        self.current = ilist[0][8]
        self.roe = ilist[0][9]
        self.total_ratio = ilist[0][10]
        self.industry = ilist[0][11]
