#Commonly Used Functions for MarketWatch-Scraper project.

import re #RegEx
from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error
import ssl #foe error handling
import time #for pauses
import datetime
import os

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
            n+=1
            continue
        if len(pelist)>0:
            pe = float(self[n+1])
            break
        else:
            pe = None
        n+=1
    print("Current Price to Earnings Ratio: ", pe)
    return(pe)

def psale_regex(self):
    n=0
    pslist=[]
    for line in self:
        #print(line)
        try:
            pslist= re.findall('(Price\sto\sSales\sRatio)',line)
        except:
            n+=1
            continue
        if len(pblist)>0:
            ps = float(self[n+1])
            break
        else:
            ps = None
        n+=1
    print("Current Price to Sales Ratio: ", ps)
    return(ps)

def pbook_regex(self):
    n=0
    pblist=[]
    for line in self:
        #print(line)
        try:
            pblist= re.findall('(Price\sto\sBook\sRatio)',line)
        except:
            n+=1
            continue
        if len(pblist)>0:
            pb = float(self[n+1])
            break
        else:
            pb = None
        n+=1
    print("Current Price to Book Ratio: ", pb)
    return(pb)

def pcf_regex(self):
    n=0
    pcflist=[]
    for line in self:
        #print(line)
        try:
            pcflist= re.findall('(Price\sto\sCash\sFlow\sRatio)',line)
        except:
            n+=1
            continue
        if len(pcflist)>0:
            pcf = float(self[n+1])
            break
        else:
            pcf = None
        n+=1
    print("Current Price to Cash Flow Ratio: ", pcf)
    return(pcf)

def ps_regex(self):
    n=0
    pslist=[]
    for line in self:
        #print(line)
        try:
            pslist= re.findall('(Price\sto\sSales\sRatio)',line)
        except:
            n+=1
            continue
        if len(pslist)>0:
            ps = float(self[n+1])
            break
        else:
            ps = None
        n+=1
    print("Current Price to Sales Ratio: ", ps)
    return(ps)

def ev_ebitda_regex(self):
    n=0
    ev_ebitdalist=[]
    for line in self:
        #print(line)
        try:
            ev_ebitdalist= re.findall('(Enterprise\sValue\sto\sEBITDA)',line)
        except:
            n+=1
            continue
        if len(ev_ebitdalist)>0:
            ev_ebitda = float(self[n+1])
            break
        else:
            ev_ebitda = None
        n+=1
    print("Current EV/EBITDA Ratio: ", ev_ebitda)
    return(ev_ebitda)

def current_ratio_regex(self):
    n=0
    current_list=[]
    for line in self:
        #print(line)
        try:
            current_list= re.findall('(Current\sRatio)',line)
        except:
            n+=1
            continue
        if len(current_list)>0:
            current_ratio = float(self[n+1])
            break
        else:
            current_ratio = None
        n+=1
    print("Current Ratio: ", current_ratio)
    return(current_ratio)

def roe_regex(self):
    n=0
    roelist=[]
    for line in self:
        #print(line)
        try:
            roelist= re.findall('(Return\son\sEquity)',line)
        except:
            n+=1
            continue
        if len(roelist)>0:
            roe = float(self[n+1])
            break
        else:
            roe = None
        n+=1
    print("Return on Equity: ", roe)
    return(roe)

def tdebt_to_tequity_regex(self):
    n=0
    total_ratio_list=[]
    for line in self:
        #print(line)
        try:
            total_ratio_list= re.findall('(P/E\sCurrent)',line)
        except:
            n+=1
            continue
        if len(total_ratio_list)>0:
            total_ratio = float(self[n+1])
            break
        else:
            total_ratio = None
        n+=1
    print("Total Debt to Total Equity Ratio: ", total_ratio)
    return(total_ratio)

def day():
    x = datetime.datetime.now()
    #y = x.year
    #y = __builtins__.str(y)
    #d = x.day
    #d = __builtins__.str(d)
    #m = x.month
    #m = __builtins__.str(m)
    #if len(d) == 1:
    #    d = '0'+ d
    #if len(m) == 1:
    #    m = '0'+ m
    #date = y+'-'+m+'-'+d
    return(x)
