#Commonly Used Functions for MarketWatch-Scraper project.

import re #RegEx
from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error
import ssl #foe error handling

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def html_retrieve(self):    #Retrieves html <p> tags from MarketWatch Profile page.
    ls = []
    url = 'https://www.marketwatch.com/investing/stock/'+self+'/profile'
    html = urllib.request.urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup('p') #May be any tag
    for tag in tags:
        try:
            ls.append(tag.string)
        except:
            continue
        #print(tags) #for troubleshooting
    return(ls)


def industry(self):         #Retrieves industry description from list variable
                            #returned by html_retrieve at line 22 (no regex)
    cnt = 0
    for line in self:
        #print(line)
        try:
            line = line.lstrip()
        except:
            continue
        cnt = cnt + 1
        bio_exist = False
        if cnt == 22:
            bio = line
            bio_exist = True
            break
        if bio_exist == False:
            bio = None
        if bio != None:
            print('==========='+'Industry'+'==========='+'\n\n'+bio)
    return(bio)

def pe_regex(self):
    n=0
    pelist=[]
    for line in self:
        #print(line)
        try:
            pelist= re.findall('(P/E\sCurrent)',line)
        except:
            continue
        if len(pelist)>0:
            pe = float(self[n+1][1:])
            break
        else:
            pe = None
        n+=1
    print("Current Price to Earnings Ratio: ", pe)
    return(pe)
