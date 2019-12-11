import sqlite3

conn = sqlite3.connect('mwdwarf.sqlite')
cur = conn.cursor()

cur.execute('SELECT Symbol FROM SP500_Data2')
list_of_stocks = cur.fetchall()

fhand = open('SP500_Data2.js', 'w')
fhand.write('sp500Json = ')

for symbol in list_of_stocks:
        cur.execute('SELECT * FROM SP500_Data2 WHERE Symbol = ?',(symbol[0],))
        data_for_symbol = cur.fetchall()
        if data_for_symbol[0][3] == None:
            pe = 'null'
        else:
            pe = str(data_for_symbol[0][3])
        if data_for_symbol[0][4] == None:
            ps = 'null'
        else:
            ps = str(data_for_symbol[0][4])
        if data_for_symbol[0][5] == None:
            pb = 'null'
        else:
            pb = str(data_for_symbol[0][5])
        if data_for_symbol[0][6] == None:
            pcf = 'null'
        else:
            pcf = str(data_for_symbol[0][6])
        if data_for_symbol[0][7] == None:
            ev = 'null'
        else:
            ev = str(data_for_symbol[0][7])
        if data_for_symbol[0][8] == None:
            current = 'null'
        else:
            current = str(data_for_symbol[0][8])
        if data_for_symbol[0][9] == None:
            roe = 'null'
        else:
            roe = str(data_for_symbol[0][9])
        if data_for_symbol[0][10] == None:
            de = 'null'
        else:
            de = str(data_for_symbol[0][10])
        if data_for_symbol[0][11] == None:
            desc = 'null'
        else:
            desc = '"'+data_for_symbol[0][11].rstrip()+'"'

        fhand.write('{\n\t"id": "'+str(data_for_symbol[0][0])+'",\n\t"date": "'+data_for_symbol[0][1]+'",\n\t"symbol": "'+data_for_symbol[0][2]+'",\n\t"priceToEarnings": '+pe+',\n\t"priceToSales": '+ps+',\n\t"priceToBook": '+pb+',\n\t"priceToCashFlow": '+pcf+',\n\t"EV/EBITDA": '+ev+',\n\t"currentRatio": '+current+',\n\t"returnOnEquity": '+roe+',\n\t"D/ERatio": '+de+',\n\t"description": '+desc+'\n}\n')

fhand.close()
