class Manager:
    def interface(self):
        print('Wellcome to your fundamentals screener\n')
        scrape_str = input('Will you be scraping data of the web(y/n):')
        scrape_str.upper()
        self.scrape_q = scrape_str
        if scrape_str == 'Y':
            list_str = input('Will you be using a self-made list(y/n):')
            list_str.upper()
            self.list_q = list_str
            if list_str == 'Y':
                list_name = input('Type the name of your list-file: \n')
                self.list_name = list_name
            if list_str == 'N':
                print('Performing updates')
            try:
                limit = int(input('How many ticker will you be scraping:'))
                self.limit
            except:
                print('This is awkard, was that a number?')
        if scrape_str == 'N':
            value_type = input('Will you be looking for under or over valued looking instruments(u/o):')
            valute_type.upper()
            self.value_type = value_type

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
        self.list_in_db = self.read_names_db()

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
