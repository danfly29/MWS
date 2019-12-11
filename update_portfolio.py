import sqlite3
import re #For regular expression
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup #For making html file prety
import ssl #foe error handling
import time #for pauses
import datetime

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def html_retrieveintofile(symbol):
    #The 'w' argument erases content of text file
    fhand = open(symbol+'.txt', 'w')
    url = 'https://finance.yahoo.com/quote/'+symbol
    html = urllib.request.urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')

    #PE ratio from yahoo is in span tag.
    tags = soup('span')
    for tag in tags:
        try:
            fhand.write(tag.string)
        except: #Necesary for No PE ratio stocks
            continue
    fhand.close()

    #Yield from yahoo is in td tag.
    return(symbol)

def price_regex(symbol):
    hand = open(symbol+'.txt',)
    for line in hand:
        #print(line)
        pelist= re.findall('.+Currency\sin\sUSD([0-9]+[.][0-9][0-9])[-+]',line)#changed regex to get last digit of price.
        if len(pelist)>0:
            pe = float(pelist[0])
            break
        else:
            pe = None
        #print("Current Price to Earnings Ratio: ", pe)
    return(pe)

conn = sqlite3.connect('mwdwarf.sqlite')
cur = conn.cursor()

cur.execute('SELECT * FROM Portfolio')
portfolio_tuple_lst = cur.fetchall()
for instrument_tuple in portfolio_tuple_lst:
    symbol = instrument_tuple[0]
    print(symbol)
    html_retrieveintofile(symbol)
    cur.execute('UPDATE Portfolio SET Price = ? WHERE Stock = ?',(price_regex(symbol), symbol))
    conn.commit()
    time.sleep(5)

cur.execute('SELECT * FROM Portfolio')
inst_tuple_lst = cur.fetchall()
total = 0
cnt = 0
amount_lst = []
for instrument in inst_tuple_lst:
    inst_tuple = inst_tuple_lst[cnt]
    print(inst_tuple)
    dolar_amount = inst_tuple[1]*inst_tuple[2]
    amount_tuple = (inst_tuple[0], dolar_amount)
    amount_lst.append(amount_tuple)
    print(inst_tuple[0],"%.2f" % dolar_amount)
    total = total + dolar_amount
    cnt = cnt + 1
print("%.2f" % total)
cnt = 0
print(inst_tuple_lst)
for instrument in inst_tuple_lst:
    inst_tuple = inst_tuple_lst[cnt]
    dolar_amount = inst_tuple[1]*inst_tuple[2]
    percentage = (dolar_amount/total)*100
    print(percentage)
    cur.execute('UPDATE Portfolio SET Percentage = ? WHERE Stock = ?', (percentage,inst_tuple[0]))
    conn.commit()
    cnt = cnt+1

stock_index_percentile = 0
stock_percentile = 0
bonds_percentile = 0
real_estate_percentile = 0
cnt = 0

for instrument in inst_tuple_lst:
    inst_tuple = inst_tuple_lst[cnt]
    if inst_tuple[3] == 'Stock Index':
        stock_index_percentile = stock_index_percentile + inst_tuple[4]
    if inst_tuple[3] == 'Stock':
        stock_percentile = stock_percentile + inst_tuple[4]
    if inst_tuple[3] == 'Bonds':
        bonds_percentile = bonds_percentile + inst_tuple[4]
    if inst_tuple[3] == 'Real Estate':
        real_estate_percentile = real_estate_percentile + inst_tuple[4]
    cnt = cnt + 1

print('Stock Index ', stock_index_percentile,'%')
print('Stock', stock_percentile,'%')
print('Bonds', bonds_percentile,'%')
print('Real Estate', real_estate_percentile, '%')
