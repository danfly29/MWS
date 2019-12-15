import re #For regular expression
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup #For making html file prety
import ssl #foe error handling



#Main Functions
def html_retrieve(self):
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


def industry(self):
    cnt = 0
    for line in self:
        print(line)
        try:
            line = line.lstrip()
        except:
            continue
        cnt = cnt + 1
        print('^^^^^^^^^^^^^'+line,cnt)
        #biolist= re.findall('^CenturyLink, Inc([+a-z0-9])',line)
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


class StockTicker:
    def load(self,i):
        self.name = i
        self.html = html_retrieve(i)
        self.industry = industry(self.html)


# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

n = StockTicker()
n.load("MU")
