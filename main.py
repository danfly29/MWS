import re #For regular expression
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup #For making html file prety
import ssl #foe error handling


class StockTicker:
    def html_retrieve(self):
        fhand = open('.txt', 'w')   #The 'w' argument erases content of text
                                    #file and avoids clutter when text files has no name
        url = 'https://www.marketwatch.com/investing/stock/'+self+'/profile'
        html = urllib.request.urlopen(url, context=ctx).read()
        soup = BeautifulSoup(html, 'html.parser')
        tags = soup('p') #May be any tag
        for tag in tags:
            try:
                fhand.write(tag.string)
            except:
                continue
            #print(tags) #for troubleshooting
            fhand.close()

    def industry(self):
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
