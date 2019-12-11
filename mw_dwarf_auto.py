#Takes oldest 50 symbols from SP500_Data2 and updates their value with  no user
#input

import sqlite3 #Database
import re #For regular expression
import urllib.request, urllib.parse, urllib.error #
from bs4 import BeautifulSoup #For making html file prety
import ssl #foe error handling
import time #for pauses
import datetime #For manipulating dates
import os #Operating system commands like running other programs


#Connect to database and create table if table is not present.
conn = sqlite3.connect('mwdwarf.sqlite')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS SP500_Data2 (id INTEGER PRIMARY KEY, Date TEXT,
 Symbol TEXT UNIQUE, PE  REAL, PS  REAL, PB  REAL, PCF  REAL,
 EVEBITDA REAL, Current  REAL, ROE REAL, DE  REAL, Description TEXT)''')


#function for retrieving html for stock symbol in marketwatch and create text
#file using BeautifulSoup.
def html_retrieveintofile(symbol):
    #The 'w' argument erases content of text file
    fhand = open('.txt', 'w')
    url = 'https://www.marketwatch.com/investing/stock/'+symbol+'/profile'
    html = urllib.request.urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')

    #PE ratio from yahoo is in span tag.
    tags = soup('p')
    for tag in tags:
        try:
            fhand.write(tag.string)
        except: #Necesary for No PE ratio stocks
            continue
    #print(tags)
    fhand.close()


#Function for returning industry description from text file retrieved trough
#html_retrieveintofile()
def industry(symbol):
    hand = open('.txt',)
    cnt = 0
    for line in hand:
        #print(line)
        line = line.lstrip()
        cnt = cnt + 1
        #print('^^^^^^^^^^^^^'+line,cnt)
        #biolist= re.findall('^CenturyLink, Inc([+a-z0-9])',line)
        bio_exist = False
        if cnt == 19:
            bio = line
            bio_exist = True
            break
        if bio_exist == False:
            bio = None
    if bio != None:
        print('==========='+'Industry'+'==========='+'\n\n'+bio)
    return(bio)

#Function that returns price to earnings using regular expressions.
def pe_regex(symbol):
    hand = open('.txt',)
    for line in hand:
        #print(line)
        pelist= re.findall('.+P/E\sCurrent([0-9.]+)P/E',line)
        if len(pelist)>0:
            pe = float(pelist[0])
            break
        else:
            pe = None
    print("Current Price to Earnings Ratio: ", pe)
    return(pe)

#function that uses regular expressions to return price to sales
def psale_regex(symbol):
    hand = open('.txt')
    for line in hand:
        #print(line)
        pslist= re.findall('.+Price\sto\sSales\sRatio([0-9.]+)Price',line)
        if len(pslist)>0:
            ps = float(pslist[0])
            break
        else:
            ps = None
    print('Price to Sales Ratio: ', ps)
    return(ps)

#function that uses regular expressions to return price to book value
def pbook_regex(symbol):
    hand = open('.txt')
    for line in hand:
        #print(line)
        pblist= re.findall('.+Price\sto\sBook\sRatio([0-9.]+)Price',line)
        if len(pblist)>0:
            pb = float(pblist[0])
            break
        else:
            pb = None
    print('Price to Book Ratio: ', pb)
    return(pb)

#function that uses regular expressions to return price to cash flow
def pcf_regex(symbol):
    hand = open('.txt')
    for line in hand:
        #print(line)
        pcflist= re.findall('.+Price\sto\sCash\sFlow\sRatio([0-9.]+)Enterprise',line)
        if len(pcflist)>0:
            pcf = float(pcflist[0])
            break
        else:
            pcf = None
    print('Price to Cash Flow Ratio: ', pcf)
    return(pcf)
#function that uses regular expressions to return Enterprise Value to Earnings Before
#Interes Taxes Depreciation and Amortization
def ev_ebitda_regex(symbol):
    hand = open('.txt')
    for line in hand:
        #print(line)
        ev_ebitdalist= re.findall('.+Enterprise\sValue\sto\sEBITDA([0-9.]+)Enterprise',line)
        if len(ev_ebitdalist)>0:
            ee = float(ev_ebitdalist[0])
            break
        else:
            ee = None
    print('Enterprise Value to EBITDA: ', ee)
    return(ee)

##function that uses regular expressions to return Current Ratio
def current_ratio_regex(symbol):
    hand = open('.txt')
    for line in hand:
        #print(line)
        crlist= re.findall('.+Current\sRatio([0-9.]+)Quick',line)
        if len(crlist)>0:
            cr = float(crlist[0])
            break
        else:
            cr = None
    print('Current Ratio: ', cr)
    return(cr)

#function that uses regular expressions to return Return on Equity
def roe_regex(symbol):
    hand = open('.txt')
    for line in hand:
        #print(line)
        roelist= re.findall('.+Return\son\sEquity([0-9.]+)Return',line)
        if len(roelist)>0:
            roe = float(roelist[0])
            break
        else:
            roe = None
    print('Return on Equity: ', roe,'%')
    return(roe)
#function that uses regular expressions to return Total Debt to Total Equity
def tdebt_to_tequity_regex(symbol):
    hand = open('.txt')
    for line in hand:
        #print(line)
        dtelist= re.findall('.+Total\sDebt\sto\sTotal\sEquity([0-9.]+)Total',line)
        if len(dtelist)>0:
            dte = float(dtelist[0])
            break
        else:
            dte = None
    print('Total Debt to Total Equity Ratio: ', dte)
    return(dte)

#Creates date in desired format
#Could be more efficient
def day():
    x = datetime.datetime.now()
    y = x.year
    y = __builtins__.str(y)
    d = x.day
    d = __builtins__.str(d)
    m = x.month
    m = __builtins__.str(m)
    if len(d) == 1:
        d = '0'+ d
    if len(m) == 1:
        m = '0'+ m
    date = y+'-'+m+'-'+d
    return(date)

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

narrowlist = [] #Empty list will be used later

#Creates list of stock ordered by date
cur.execute('''SELECT Symbol FROM SP500_Data2 ORDER BY Date''')
list_of_symbols_by_date = cur.fetchall()

#Creates list of the 50 stocks that have not been updated for the longest. Or if
#more than 50 have the same oldest entry date selects by alphabetical.
cnt = 0
while cnt < 500:
    narrowlist.append(list_of_symbols_by_date[cnt][0])
    cnt = cnt + 1

#Heart of algorithm.
#Selects one of 50 stock symbols on narrowlist and
iteration = 0
for symbol in narrowlist:
    print('Stock:' + symbol , (iteration + 1))

    #cur.execute('SELECT * FROM SP500_Data2 WHERE Symbol = ?',(symbol,))
    #existing_stock = cur.fetchall()
    #if len(existing_stock) > 0:
    html_retrieveintofile(symbol)
    description = industry(symbol)
    print('==========='+'Measures of Value'+'==========='+'\n')
    cur.execute('''UPDATE SP500_Data2 SET Date = ?,
        PE = ?, PCF = ?, PB = ?,  PS = ?,
        EVEBITDA = ?, Current = ?, ROE = ?, DE = ?, Description = ?
        WHERE Symbol = ?
         ''',(day(),pe_regex(symbol),pcf_regex(symbol),pbook_regex(symbol),psale_regex(symbol),ev_ebitda_regex(symbol),current_ratio_regex(symbol),roe_regex(symbol),tdebt_to_tequity_regex(symbol), description, symbol))
    iteration = iteration + 1
        #os.remove(symbol+".txt")
    if iteration%4 == 0 and iteration != 0:
        print('================================================================')
        conn.commit()
        time.sleep(30)

    if iteration == 500:
        break
conn.commit()
print('Data for', iteration, 'Stock was commited' )
