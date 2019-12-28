import re #For regular expression
from bs4 import BeautifulSoup #For making html file prety
import time #for pauses

from functions import *
from mws_classes import *



manager = Manager()
ticker = StockTicker()
manager.initiate_db()
manager.interface()

iteration= 0
if manager.scrape_q == 'Y':
    if manager.list_q == 'N':
        for line in manager.list_in_db:
            ticker.scrape(line)
            manager.update(ticker)
            iteration +=1
            if iteration == manager.limit:
                break
            if iteration%4 == 0 and iteration != 0:
                print('===================Taking a Nap=====================')
                time.sleep(30)
    if manager.list_q == 'Y':
        for line in manager.list_in_db:
            ticker.scrape(line)
            try:
                manager.update(ticker)
            except:
                manager.save(ticker)
            iteration +=1
            if iteration == manager.limit:
                break
            if iteration%4 == 0 and iteration != 0:
                print('===================Taking a Nap=====================')
                time.sleep(30)

if manager.scrape_q == 'N':
    if manager.value_type == 'U':
        print(1)
        for line in manager.list_in_db:
            ticker.reload(line)
            manager.screener(ticker)
        if len(manager.screener_result)>0:
            print(len(manager.screener_result), 'Passed')
            print('-----------------------------------------------------')
            for line in manager.screener_result:
                ticker.reload(line)
                manager.printer(ticker)
