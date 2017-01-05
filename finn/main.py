#!/usr/bin/env python
# -*- coding: utf-8 -*-



import time, re, sys, os, random, requests
from multiprocessing.dummy import Pool 
from bs4 import BeautifulSoup as BS

## Define constant variables;
URL = "http://m.finn.no/lookup.html?finnkode="
wd = "/home/tian/Finn/pages/"
log = "/home/tian/Finn/log"


def download_page(finn_code):
    url = URL + str(finn_code)
    r = ""
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            html = r.content
            bs = BS(html)
            try:
                div_menu = bs.find("div", {"class": "flex-grow1 truncate mrl flex"}).findAll("a")
                dir_menu = div_menu[0].get_text().encode('utf8', 'replace')
                if (len(div_menu) >= 2):
                    for m in range(1, len(div_menu)):
                        dir_menu = dir_menu + "/" + div_menu[m].get_text().encode('utf8', 'replace')
                file_name = wd + dir_menu + "/" + str(finn_code) + ".html"
                ## If the directory not exist, then create first;
                if not os.path.exists(os.path.dirname(file_name)):
                    os.makedirs(os.path.dirname(file_name))
                ## Save HTML file to disk
                with open(file_name, "w") as f:
                    f.write(html)
                    f.close()
                ## Random sleep seconds
                time.sleep(random.uniform(1,3))
                with open(log, "a") as l:
                    l.write(str(finn_code)+" OK\n")
                    l.close()
                ## Message
                msg = "\rCode " + str(finn_code) + " saved to: " + str(file_name) + " \n"
                sys.stdout.write(msg); sys.stdout.flush()     
            except:
                with open(log, "a") as l:
                    l.write(str(finn_code)+" Error\n")
                    l.close()
                msg = "\rCode " + str(finn_code) + " encounts an error!\n"
                sys.stdout.write(msg); sys.stdout.flush()  
        else:
            with open(log, "a") as l:
                l.write(str(finn_code)+" NA\n")
                l.close()
            msg = "\rCode " + str(finn_code) + " not exist!\n"
            sys.stdout.write(msg); sys.stdout.flush()
    except:
        with open(log, "a") as l:
            l.write(str(finn_code)+" ConnectError\n")
            l.close()
        msg = "\rCode " + str(finn_code) + " encounts an error!\n"
        sys.stdout.write(msg); sys.stdout.flush()   
        time.sleep(61)     



N1 = int(sys.argv[1])
N2 = int(sys.argv[2])
kode_all = range(N1, N2)

kode_downloaded = []
f = open('/home/tian/Finn/log', 'r')
for line in f:
        kode_downloaded.append(int(line[0:8]))

f.close()
kodes = list(set(kode_all) - set(kode_downloaded))
pool = Pool(8)
pool.map(download_page, kodes) 
pool.close()  
pool.join()  


