#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time, re, sys, os, random, requests
from multiprocessing.dummy import Pool 
from bs4 import BeautifulSoup as BS

## Define constant variables;
URL = "https://m.finn.no/lookup.html?finnkode="
dir_prj = "/home/tian/1T/Finn/"

## Unit: 10 million
codeLen = 10000000
arg = sys.argv[1]
codeFirst = codeLen * (int(arg) + 0)
if len(sys.argv) == 2:
    codeLast  = codeLen * (int(arg) + 1) 
if len(sys.argv) == 3:
    codeLast  = codeLen * (int(float(sys.argv[2])) + 1) 

## Generate directory and log
pag = dir_prj + "pages_" + arg + "/"
log = dir_prj + "log_" + arg

if not os.path.exists(pag):
    os.makedirs(pag)

if not os.path.exists(log):
    os.system("touch " + log)

    
proxies_ls = [
    "https://91.200.83.107:8085",
    "https://91.204.14.113:8085",
    "https://146.185.204.70:8085",
    "https://193.105.171.7:8085"] 


####### Record log
def write_log(finn_code, msg):
    with open(log, "a") as l:
        l.write(str(finn_code) + " " +  msg + " " + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) + "\n")
        l.close()
    print  "\rKey: " + str(finn_code) + " " + msg + "!"


def download_page(finn_code):
    url = URL + str(finn_code)
    try:
        proxy = {"https" : proxies_ls[id % len(proxies_ls)]}
        r = requests.get(url, proxies = proxy, timeout=5)
        if r.status_code == 200:
            html = r.content
            bs = BS(html)
            try:
                div_menu = bs.find("div", {"class": re.compile("flex-grow1 truncate mrl flex.*")}).findAll("a")
                dir_menu = div_menu[0].get_text().encode('utf8', 'replace')
                if (len(div_menu) >= 2):
                    for m in range(1, len(div_menu)):
                        dir_menu = dir_menu + "/" + div_menu[m].get_text().encode('utf8', 'replace')
                file_name = pag + dir_menu + "/" + str(finn_code) + ".html"
                ## If the directory not exist, then create first;
                if not os.path.exists(os.path.dirname(file_name)):
                    os.makedirs(os.path.dirname(file_name))
                ## Save HTML file to disk
                with open(file_name, "w") as f:
                    f.write(html)
                    f.close()
                ## Random sleep seconds
                time.sleep(1)
                write_log(finn_code, "OK " + file_name)    
            except:
                write_log(finn_code, "ParseError")  
        elif r.status_code == 403:
            global id
            id = id + 1
            sleep(1)
        else:
            write_log(finn_code, "NotExist")
    except:
        write_log(finn_code, "RequestError")   




id = 1

## Total codes;
codes_all = range(codeFirst, codeLast)
## Tried codes;
codes_tried = []
with open(log, "r") as f:
    for line in f:
        codes_tried.append(int(line[0:8]))
    f.close()
## Codes not tried;
codes_untried = list(set(codes_all) - set(codes_tried))


codes_downloaded = []
with open(log, "r") as f:
    for line in f:
        if line[9:10] == "O" or line[9:10] == "N" or line[9:10] == "P":
            codes_downloaded.append(int(line[0:8]))
    f.close() 
codes_redownload = list(set(codes_all) - set(codes_downloaded))

    
if len(codes_untried) > 0:
    print "There are " + str(len(codes_untried)) + " codes need to download!"
    time.sleep(5)    
    pool = Pool(16)
    pool.map(download_page, codes_untried) 
    pool.close()  
    pool.join() 
elif len(codes_redownload) > 0:
    print "There are " + str(len(codes_redownload)) + " codes need to redownload!"
    time.sleep(5)   
    pool = Pool(8)
    pool.map(download_page, codes_redownload) 
    pool.close()  
    pool.join()
else:
    print "All codes have been downloaded!"



