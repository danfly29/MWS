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

#Gets previous quarter portfolio balance from
def old_balance():
    cur.execute('SELECT * FROM Value_Averaging_Balance_Sheet')
    balance_lst = cur.fetchall()
    size_balance_lst = len(balance_lst)
    if size_balance_lst == 0:
        last_balance = 0
    if size_balance_lst > 0:
        last_balance_row = balance_lst[size_balance_lst-1]
        last_balance = last_balance_row[5]
    return(last_balance)

#Determines how much cash must be placed in or out for 3% growht
def cash_flow(old_balance,current_value):
    try:
        cash_flow = (old_balance*1.03 - current_value)*-1
    except:
        cash_flow = None
    return(cash_flow)

def old_cash_balance():
    cur.execute('SELECT * FROM Value_Averaging_Balance_Sheet')
    balance_lst = cur.fetchall()
    size_balance_lst = len(balance_lst)
    if size_balance_lst == 0:
        last_cash_balance = 0
    if size_balance_lst > 0:
        
        last_cash_balance_row = balance_lst[size_balance_lst-1]
        last_cash_balance = last_cash_balance_row[4]
    return(last_cash_balance)

def new_cash_balance(old_cash_balance,cash_flow):
    new_cash_balance = old_cash_balance + cash_flow
    return(new_cash_balance)

def day():
    x = datetime.datetime.now()
    y = x.year
    y = __builtins__.str(y)
    m = x.month
    m = __builtins__.str(m)
    d = x.day
    d = __builtins__.str(d)
    date = d+'-'+m+'-'+y
    return(date)

#Retrieves span tags from yahoofinancials overview for stock
def html_retrieveintofile(symbol):
    #The 'w' argument erases content of text file
    fhand = open(symbol+'.txt', 'w')
    url = 'https://finance.yahoo.com/quote/'+symbol
    html = urllib.request.urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')


    tags = soup('span')
    #print(tags)
    for tag in tags:
        #print(tag)
        try:
            fhand.write(tag.string)
        except: #Necesary for No PE ratio stocks
            continue
    fhand.close()

    #Yield from yahoo is in td tag.
    return(symbol)

#retrives the price on the file with span tags from yahoofinancials overview
def price_regex(symbol):
    hand = open(symbol+'.txt',)
    for line in hand:
        print(line)
        pelist= re.findall('.+Currency\sin\sUSD([0-9]+[.][0-9][0-9]?)',line)#changed regex to get last digit of price.
        if len(pelist)>0:
            pe = float(pelist[0])
            break
        else:
            pe = None
    #print("Current Price to Earnings Ratio: ", pe)
    return(pe)

def category_giver(integer):
            if integer == 1:
                category = 'Stock'
            if integer == 2:
                category = 'Stock Index'
            if integer == 3:
                category = 'Bonds'
            if integer == 4:
                category = 'Real Estate'

conn = sqlite3.connect('mwdwarf.sqlite')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Portfolio (Stock TEXT, Quantity INT,
    Price REAL, Category TEXT)''')#Does not need to run if table exists

ask = True
cnt = 0
while ask == True:
    acquisition = input('Enter YES if stocks where bought\n')
    if acquisition == 'YES':
        cnt = cnt + 1
        symbol = input('Enter stock symbol: ')
        html_retrieveintofile(symbol)

        quantity = input('Enter Quantity bought: ')
        cat_int = int(input('''Enter Category: \n 1 for Stock\n 2 for Stock Index\n 3 for Bonds\n 4 for Real Estate\n\n'''))
        cur.execute('SELECT * FROM Portfolio WHERE Stock = ?', (symbol,))
        inst_tuple_lst = cur.fetchall()
        print(inst_tuple_lst)

        if len(inst_tuple_lst) == 0:
            #print(inst_tuple_lst)
            cur.execute('''INSERT INTO Portfolio(Stock, Quantity, Price, Category) VALUES(?,?,?,?)''',(symbol,quantity,price_regex(symbol),category_giver(cat_int)))
            conn.commit()
        if len(inst_tuple_lst) == 1:
            cur.execute('SELECT * FROM Portfolio WHERE Stock = ?',(symbol,))
            old_inst_tuple_ls = cur.fetchall()
            old_inst_tuple = old_inst_tuple_ls[0]
            new_quant = old_inst_tuple[1] + quantity
            cur.execute('''UPDATE Portfolio SET Quantity = ? WHERE Stock = ?''',(new_quant, symbol))
    if acquisition == 'NO':
        cur.execute('SELECT * FROM Portfolio')
        portfolio_tuple_lst = cur.fetchall()
        for instrument_tuple in portfolio_tuple_lst:
            symbol = instrument_tuple[0]
            print(symbol)
            html_retrieveintofile(symbol)
            cur.execute('UPDATE Portfolio SET Price = ? WHERE Stock = ?',(price_regex(symbol), symbol))
            conn.commit()
            time.sleep(5)
        ask = False
    else:
        ask = False

print(cnt, 'Transactions Commited')


#Determine instruments stake in portfolio
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

cur.execute('''CREATE TABLE IF NOT EXISTS Value_Averaging_Balance_Sheet
    ( ID INT AUTO_INCREMENT PRIMARY KEY, Date TEXT, Current_Value INT, Cash_Flow INT, New_Cash_Balance INT,
    New_Balance INT)''')


old_bl = old_balance()
cash_f = cash_flow(old_bl,total)
new_cash_b = int(new_cash_balance(old_cash_balance(),cash_f))
cur.execute('''INSERT INTO Value_Averaging_Balance_Sheet (Date, Current_Value,
Cash_Flow, New_Cash_Balance, New_Balance) VALUES(?,?,?,?,?) ''', (day(), int(total), int(cash_f),new_cash_b,int(old_bl*1.03)))

conn.commit()
