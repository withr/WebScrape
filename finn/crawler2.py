#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time, re, sys, os, random, subprocess, requests
from multiprocessing.dummy import Pool 
from bs4 import BeautifulSoup as BS


folder = "/home/tian/1T/Finn/pages_6/"
shellMSG = subprocess.check_output("find " + folder + " -type f", shell=True)
html_ls =  shellMSG.split('\n')[:-1]
N = len(html_ls)

URL = "https://m.finn.no/lookup.html?finnkode="


def recrawl(i):
    html = html_ls[i]
    n = subprocess.check_output('ls -l "' + html + '" | awk  \'{print $5}\'', shell=True)
    if int(n) < 50:
        finn_code = html[-13:-5]
        url = URL + str(finn_code)
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            with open(html, "w") as f:
                    f.write(r.content)
                    f.close()
            print "Recrawl " + str(i) + ": "+ html_ls[i]

for i in range(N):
    recrawl(i)
    msg = "\rDone: " + str(i) + "; percent: " + str(i/float(N))
    sys.stdout.write(msg); sys.stdout.flush()


