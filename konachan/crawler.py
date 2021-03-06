#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time, re, sys, os,  requests
from multiprocessing.dummy import Pool 
from bs4 import BeautifulSoup as BS

## Define constant variables;
URL = "https://m.finn.no/lookup.html?finnkode="
dir_prj = "/home/tian/GAN_demo/"

codeLen = 10000000
codeFirst = int(sys.argv[1]) * codeLen
codeLast  = int(sys.argv[1]) * codeLen + codeLen

pag = dir_prj + "pages_" + sys.argv[1] + "/"
log = dir_prj + "log_" + sys.argv[1]

proxies_ls = [
    "https://37.9.45.242:8085",
    "https://91.243.94.120:8085",
    "https://93.179.89.230:8085",
    "https://146.185.204.86:8085",
    "https://91.243.89.89:8085"] 

proxy = {"https": proxies_ls[int(sys.argv[1]) % len(proxies_ls)]}


####### Record log
def write_log(finn_code, msg):
    with open(log, "a") as l:
        l.write(str(finn_code) + " " +  msg + " " + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) + "\n")
        l.close()
    print  "\rPostnumber: " + str(finn_code) + " " + msg + "!"


def download_page(finn_code):
    url = URL + str(finn_code)
    try:
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
        else:
            write_log(finn_code, "NotExist")
    except:
        write_log(finn_code, "RequestError")   

        
if len(sys.argv) > 2:
    codes_all = []
    with open(log, "r") as f:
        for line in f:
            if line[9:10] != "O" and line[9:10] != "N":
                codes_all.append(int(line[0:8]))
        f.close()
    codes_downloaded = []
    global log
    log = dir_prj + ".log_" + sys.argv[1]
    with open(log, "r") as f:
        for line in f:
            if line[9:10] == "O" or line[9:10] == "N":
                codes_downloaded.append(int(line[0:8]))
        f.close() 
    ## Codes plan to download;
    codes = list(set(codes_all) - set(codes_downloaded)) 
    print "There are " + str(len(codes)) + " codes need to redownload!"
    time.sleep(5)
    ## Main;
    pool = Pool(8)
    pool.map(download_page, codes) 
    pool.close()  
    pool.join()
else:
    ## Total codes;
    codes_all = range(codeFirst, codeLast)
    ## Downloaded/tried codes;
    codes_downloaded = []
    with open(log, "r") as f:
        for line in f:
            codes_downloaded.append(int(line[0:8]))
        f.close()
    ## Codes plan to download;
    codes = list(set(codes_all) - set(codes_downloaded))
    print "There are " + str(len(codes)) + " codes need to download!"
    time.sleep(5)    
    ## Main;
    pool = Pool(8)
    pool.map(download_page, codes) 
    pool.close()  
    pool.join()  

##import subprocess 
##output = subprocess.check_output("find /home/tian/Finn/pages_8 -type f", shell=True)
##file_ls <- output.split('\n')



import os, requests
from bs4 import BeautifulSoup as BS
import os
import traceback

def download(url, filename):
    if os.path.exists(filename):
        print('file exists!')
        return
    try:
        r = requests.get(url, stream=True, timeout=60)
        r.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()
        return filename
    except KeyboardInterrupt:
        if os.path.exists(filename):
            os.remove(filename)
        raise KeyboardInterrupt
    except Exception:
        traceback.print_exc()
        if os.path.exists(filename):
            os.remove(filename)


if os.path.exists('imgs') is False:
    os.makedirs('imgs')

start = 1
end = 8000
for i in range(start, end + 1):
    url = 'http://konachan.net/post?page=%d&tags=' % i
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    for img in soup.find_all('img', class_="preview"):
        target_url = 'http:' + img['src']
        filename = os.path.join('imgs', target_url.split('/')[-1])
        download(target_url, filename)
    print('%d / %d' % (i, end))
