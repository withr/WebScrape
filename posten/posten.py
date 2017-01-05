#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import *
import re, sys, os, random, requests 
from bs4 import BeautifulSoup as BS

## Define constant variables;
URL = "https://adressesok.posten.no/nb/addresses/search?view=list&q=postnummer%3A"
wd  = "/home/tian/Posten/pages/"
log = "/home/tian/Posten/log"

## Record log
def write_log(postnr, msg):
    log = "/home/tian/Posten/log"
    with open(log, "a") as l:
        l.write(postnr + " " +  msg + " " + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + "\n")
        l.close()
    print  "\rPostnumber: " + postnr + " " + msg + "!"

## 
def download_page(postnr):
    url = URL + postnr
    notDownloaded = True
    t1 = time()
    while notDownloaded:
        r = requests.get(url, timeout=5)
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
            sleep(60)
            msg = "\rPostnumber " + postnr + " try later!" + " waited " + str(int(time()-t1)) + " seconds."
            sys.stdout.write(msg); sys.stdout.flush() 


## postnr_all
p1 = int(sys.argv[1])
p2 = int(sys.argv[2])
postnr_all = []
xx = range(p1, p2)
for i in range(len(xx)):
    postnr_all.append('{:04d}'.format(xx[i]))

## postnr_downloaded
postnr_downloaded = []
f = open('/home/tian/Posten/log', 'r')
for line in f:
    postnr_downloaded.append(line[0:4])

f.close()

## postnr_todownload
postnr_todownload = list(set(postnr_all) - set(postnr_downloaded))
postnr_todownload.sort()

print "postnr_all: " + str(len(postnr_all))
print "postnr_downloaded: " + str(len(postnr_downloaded))
print "postnr_todownload:" + str(len(postnr_todownload))

for postnr in postnr_todownload:
    download_page(postnr)


