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
