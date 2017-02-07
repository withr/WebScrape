#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import *
import re, sys, os, random, requests
from bs4 import BeautifulSoup as BS
from multiprocessing.dummy import Pool


## Define constant variables;
URL = "https://adressesok.posten.no/nb/addresses/search?view=list&q=postnummer%3A"
Prj = "/home/tian/HDD3T/Posten/"
ext = "" if len(sys.argv) < 2 else "_" + sys.argv[1]
pag = Prj + "crawled" + ext + "/"
log = Prj + "crawled" + ext + ".log"   
## If folder/log file not exist, create.   
if not os.path.exists(pag): os.makedirs(pag)

if not os.path.exists(log): os.system("touch " + log)


## Record log
def write_log(key, msg):
    with open(log, "a") as l:
        l.write(key + "\t" +  msg + "\t" + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + "\n")
        l.close()
    print "\rPostnumber: " + key + " " + msg + "!"


proxies_ls = [
    "https://91.200.83.107:8085",
    "https://91.243.94.107:8085",
    "https://91.204.14.113:8085",
    "https://146.185.204.70:8085",
    "https://193.105.171.7:8085"] 
    
## Global ID for proxy to be used;    
ID = 0
Exe = True; ## 
 
def download_page(key):
    url = URL + key
    N = 0
    while Exe and N < len(proxies_ls):
        id = ID
        proxies = {"https" : proxies_ls[id]}
        r = requests.get(url, proxies = proxies, timeout=5)
        if r.status_code == 200:
            html = r.content
            bs = BS(html) 
            search_count = bs.find("h2", {"class": "search_count"}).get_text().encode('utf8', 'replace')
            search_count = re.sub("^ *", "", search_count)
            search_parse = search_count.split(" ")
            if search_parse[1] == "adresser" and search_parse[0] != "0":
                file_name = pag + key + ".html"
                #with open(file_name, "w") as f:
                #    f.write(html)
                #    f.close()
                write_log(key, "OK")
            else:
                write_log(key, "NoAddress")
            N = len(proxies_ls); ## stop while loop
        else:
            proxy_1 = proxies_ls[id]
            global ID
            ID = (id + 1) % len(proxies_ls)
            proxy_2 = proxies_ls[ID]
            N = N + 1
            if N == len(proxies_ls):
                global Exe
                Exe = False
            print "\rPostnumber " + key + ": IP (" + proxy_1 + ") was baned, try to use new one!" + " (" + proxy_2 + ")"

    
keys = []
for i in range(1500, 8800):
    key = '{:04d}'.format(i)
    print key
    download_page(key)
    keys.append('{:04d}'.format(i))    


pool = Pool(8)
pool.map(download_page, keys) 
pool.close()  
pool.join()

