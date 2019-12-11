import sqlite3
import re #For regular expression
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup #For making html file prety
import ssl #foe error handling
import time #for pauses

conn = sqlite3.connect('mwdwarf.sqlite')
cur = conn.cursor()

cur.execute('SELECT * FROM SP500_Data2')
inst_tuple_lst = cur.fetchall()

try:
    PriceToEarnings = float(input('Enter the maximum Price to Earnings Ratio\n  '))
except:
    PriceToEarnings = 18

try:
    PriceToSales = float(input('Enter the maximum Price to Sales Ratio\n  '))
except:
    PriceToSales = 2.33

try:
    PriceToBook = float(input('Enter the maximum Price to Book\n  '))
except:
    PriceToBook = 2.86

try:
    PriceToCashFlow = float(input('Enter the maximum Price to Cash Flow\n  '))
except:
    PriceToCashFlow = 12.6

try:
    EVtoEBITDA = float(input('Enter the maximum Enterprise Value to EBITDA\n  '))
except:
    EVtoEBITDA = 10

try:
    CurrentRatio = float(input('Enter the minimum current Ratio\n  '))
except:
    CurrentRatio = 1.1

try:
    ROE =  float(input('Enter the minimum Return On Equity\n  '))
except:
    ROE = 15

try:
    TotalDebToTotalEquity = float(input('Enter the maximum Total Debt to Total Equity\n  '))
except:
    TotalDebToTotalEquity = 50

selected_inst_tuple_lst = []

for instrument in inst_tuple_lst:
    present_value = 0
    print(instrument[2])
    if instrument[3] != None:
        if instrument[3] > PriceToEarnings: #Evaluates price to earnings ratios
            print('Droped at P/E')
            continue
        present_value = present_value + 1
    if instrument[4] != None:
        if instrument[4] > PriceToSales: #Evaluates price to sales ratios
            print('Droped at P/S')
            continue
        present_value = present_value + 1
    if instrument[5] != None:
        if instrument[5] > PriceToBook: #Evaluates price to book ratios
            print('Droped at P/B')
            continue
        present_value = present_value + 1
    if instrument[6] != None:
        if instrument[6] > PriceToCashFlow: #Evaluates price to cash flow
            print('Droped at P/CF')
            continue
        present_value = present_value + 1
    if instrument[7] != None:
        if instrument[7] > EVtoEBITDA: # Evaluates EV/EBITDA
            print('Droped at EV/EBITDA')
            continue
        present_value = present_value + 1
    if instrument[8] != None:
        if instrument[8]< CurrentRatio: #Evaluates CurrentRatio
            print('Droped at CurrentRatio')
            continue
        present_value = present_value + 1
    if instrument[9] != None:
        if instrument[9] < ROE: #evaluates ReturnOnEquity
            print('Droped at ROE')
            continue
        present_value = present_value + 1
    if instrument[10] != None:
        if instrument[10] > TotalDebToTotalEquity: #Evaluates Total Debt to Total Equity
            print('Droped at Total Debt to Total Equity')
            continue
        present_values = present_value + 1

    if present_value > 4:
        selected_inst_tuple_lst.append(instrument)
fhand = open('favorites.json', 'w')
for selected_inst_tuple in selected_inst_tuple_lst:
    print('\nStock:', selected_inst_tuple[2], "  as of: ", selected_inst_tuple[1])
    print("=======================================")
    print('Price to Earnings:', selected_inst_tuple[3])
    print('Price to Sales:', selected_inst_tuple[4])
    print("Price to Book:", selected_inst_tuple[5])
    print("Price to Cash Flow:", selected_inst_tuple[6])
    print("EV/EBITDA:", selected_inst_tuple[7])
    print("Current Ratio:", selected_inst_tuple[8])
    print("ROE:", selected_inst_tuple[9])
    print("Total Debt to Total Equity:", selected_inst_tuple[10])
    print("\n")
    if selected_inst_tuple[3] == None:
        pe = 'null'
    else:
        pe = str(selected_inst_tuple[3])
    if selected_inst_tuple[4] == None:
        ps = 'null'
    else:
        ps = str(selected_inst_tuple[4])
    if selected_inst_tuple[5] == None:
        pb = 'null'
    else:
        pb = str(selected_inst_tuple[5])
    if selected_inst_tuple[6] == None:
        pcf = 'null'
    else:
        pcf = str(selected_inst_tuple[6])
    if selected_inst_tuple[7] == None:
        ev = 'null'
    else:
        ev = str(selected_inst_tuple[7])
    if selected_inst_tuple[8] == None:
        current = 'null'
    else:
        current = str(selected_inst_tuple[8])
    if selected_inst_tuple[9] == None:
        roe = 'null'
    else:
        roe = str(selected_inst_tuple[9])
    if selected_inst_tuple[10] == None:
        de = 'null'
    else:
        de = str(selected_inst_tuple[10])
    if selected_inst_tuple[11] == None:
        desc = 'null'
    else:
        desc = '"'+selected_inst_tuple[11].rstrip()+'"'

    fhand.write('{\n\t"id": "'+str(selected_inst_tuple[0])+'",\n\t"date": "'+selected_inst_tuple[1]+'",\n\t"symbol": "'+selected_inst_tuple[2]+'",\n\t"priceToEarnings": '+pe+',\n\t"priceToSales": '+ps+',\n\t"priceToBook": '+pb+',\n\t"priceToCashFlow": '+pcf+',\n\t"EV/EBITDA": '+ev+',\n\t"currentRatio": '+current+',\n\t"returnOnEquity": '+roe+',\n\t"D/ERatio": '+de+',\n\t"description": '+desc+'\n}\n')
