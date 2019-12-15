#Commonly Used Functions for MarketWatch-Scraper project.

import re #RegEx
from bs4 import BeautifulSoup

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
