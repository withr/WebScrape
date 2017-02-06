#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import *
import re, sys, os, random, requests
from bs4 import BeautifulSoup as BS


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
    
ID_proxy = 0    
def download_page(postnr):
    url = URL + postnr
    Nr_tried = 0
    while Nr_tried < len(proxies_ls):
        proxies = {"https" : proxies_ls[id % 5]}
        r = requests.get(url, proxies = proxies, timeout=5)
        sleep(1)
        html = r.content
        bs = BS(html)
        try:
            search_count = bs.find("h2", {"class": "search_count"}).get_text().encode('utf8', 'replace')
            search_count = re.sub("^ *", "", search_count)
            search_parse = search_count.split(" ")
            if search_parse[1] == "adresser" and search_parse[0] != "0":
                file_name = wd + postnr + ".html"
                with open(file_name, "w") as f:
                    f.write(html)
                    f.close()
                write_log(postnr, "OK")
            else:
                write_log(postnr, "NoAddress")
            notDownloaded = False
        except:
            global id
            id = id + 1
            sleep(1)
            msg = "\rPostnumber " + postnr + " try later!" + " waited " + str(int(time()-t1)) + " seconds."
            sys.stdout.write(msg); sys.stdout.flush()
        ID_proxy += ID_proxy
    else:
        break
    
    
    
