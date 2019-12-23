import re #For regular expression
from bs4 import BeautifulSoup #For making html file prety
import time #for pauses

from functions import *
from mws_classes import *



manager = Manager()
manager.initiate_db()
manager.list_in_db
manager.interface()
iteration= 0
if manager.scrape_q == 'Y':
    if manager.list_q == 'N':
        for line in manager.list_in_db:
            ticker = StockTicker()
            ticker.scrape(line)
            manager.update(ticker)
            iteration +=1
            if iteration == manager.limit:
                break
            if iteration%4 == 0 and iteration != 0:
                print('===================Taking a Nap=====================')
                time.sleep(30)
