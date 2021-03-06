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
            if line == 'P/E Current':
                bio = 'Error 21'
                break
            bio = line
            bio_exist = True
            break
        if bio_exist == False:
            bio = None
        #if bio != None:
            #print('==========='+'Industry'+'==========='+'\n\n'+bio)
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
            try:
                pe = self[n+1]
                pe = pe.replace(',','')
                pe = float(pe)
            except:
                pe = None
            break
        else:
            pe = None
        n+=1
    #print("Current Price to Earnings Ratio: ", pe)
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
            ps = self[n+1]
            if type(ps) == str:
                ps = ps.replace(',','')
            ps = float(ps)
            break
        else:
            ps = None
        n+=1
    #print("Current Price to Sales Ratio: ", ps)
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
            pb = self[n+1]
            if type(pb) == str:
                pb = pb.replace(',','')
            pb = float(pb)
            break
        else:
            pb = None
        n+=1
    #print("Current Price to Book Ratio: ", pb)
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
            pcf = self[n+1]
            if type(pcf) == str:
                pcf = pcf.replace(',','')
            pcf = float(pcf)
            break
        else:
            pcf = None
        n+=1
    #print("Current Price to Cash Flow Ratio: ", pcf)
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
            ps = self[n+1]
            if type(ps) == str:
                ps = ps.replace(',','')
            ps = float(ps)
            break
        else:
            ps = None
        n+=1
    #print("Current Price to Sales Ratio: ", ps)
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
            ev_ebitda = self[n+1]
            if type(ev_ebitda) == str:
                ev_ebitda = ev_ebitda.replace(',','')
            ev_ebitda = float(ev_ebitda)
            break
        else:
            ev_ebitda = None
        n+=1
    #print("Current EV/EBITDA Ratio: ", ev_ebitda)
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
            current_ratio = self[n+1]
            if type(current_ratio) == str:
                current_ratio = current_ratio.replace(',','')
            current_ratio = float(current_ratio)
            break
        else:
            current_ratio = None
        n+=1
    #print("Current Ratio: ", current_ratio)
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
            roe = self[n+1]
            try:
                roe = roe.replace(',','')
            except:
                continue
            roe = float(roe)
            break
        else:
            roe = None
        n+=1
    #print("Return on Equity: ", roe)
    return(roe)

def tdebt_to_tequity_regex(self):
    n=0
    total_ratio_list=[]
    for line in self:
        #print(line)
        try:
            total_ratio_list= re.findall('(Total\sDebt\sto\sTotal\sEquity)',line)
        except:
            n+=1
            continue
        if len(total_ratio_list)>0:
            total_ratio=self[n+1]
            try:
                total_ratio = total_ratio.replace(',','')
            except:
                continue
            total_ratio = float(total_ratio)
            break
        else:
            total_ratio = None
        n+=1
    #print("Total Debt to Total Equity Ratio: ", total_ratio)
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
