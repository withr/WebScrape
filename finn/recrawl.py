#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time, re, sys, os, random, subprocess, requests
from multiprocessing.dummy import Pool 


URL = "https://m.finn.no/lookup.html?finnkode="
proxies_ls = [
    "https://91.200.83.107:8085",
    "https://91.243.94.107:8085",
    "https://91.204.14.113:8085",
    "https://146.185.204.70:8085",
    "https://193.105.171.7:8085"] 
arg = sys.argv[1]
proxy = {"https" : proxies_ls[int(arg) % len(proxies_ls)]}


folder = "/home/tian/1T/Finn/pages_" + arg + "/"
Id_log = "/home/tian/1T/Finn/pages_" + arg + "_retry"
Id_lst = "/home/tian/1T/Finn/pages_" + arg + "_list"

if not os.path.exists(Id_log):
    os.system("touch " + Id_log)

if not os.path.exists(Id_lst):
    os.system("touch " + Id_lst)


shellMSG = open(Id_lst).read()
if len(shellMSG) < 10:
    shellMSG = subprocess.check_output("find " + folder + " -type f", shell=True)
    with open(Id_lst, "w") as f: 
        f.write(shellMSG); 
        f.close()

html_ls =  shellMSG.split('\n')[:-1]  
N = len(html_ls)


def recrawl(i):
    html = html_ls[i]
    n = subprocess.check_output('ls -l "' + html + '" | awk  \'{print $5}\'', shell=True)
    msg = "\rId: " + str(i) + "; Code: " + html[-13:-5] + "; size: " + str(int(n))
    sys.stdout.write(msg); sys.stdout.flush()
    if int(n) < 100:
        finn_code = html[-13:-5]
        url = URL + str(finn_code)
        try:
            r = requests.get(url, proxies = proxy, timeout=5)
            if r.status_code == 200:
                with open(html, "w") as f:
                        f.write(r.content)
                        f.close()
            print "\nRecrawl: " + html[-13:-5] + "; status_code:" + str(r.status_code) + "; original size: " + str(int(n)) + "; new size: " + str(len(r.content))
        except:
            sys.stdout.write("\rConnection rejected!"); sys.stdout.flush()
    with open(Id_log, "a") as f: 
        f.write(str(i)+'\n'); 
        f.close()

id_tried = []
with open(Id_log, "r") as f:
    for line in f:
        id_tried.append(int(line))
    f.close()

id_total = range(N)
id_crawl = list(set(id_total) - set(id_tried))
len(id_tried)/float(N)

pool = Pool(8)
pool.map(recrawl, id_crawl) 
pool.close()  
pool.join()


