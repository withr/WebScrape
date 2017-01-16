#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time, re, sys, os, random, requests
from multiprocessing.dummy import Pool 
from bs4 import BeautifulSoup as BS

## Define constant variables;
URL = "https://m.finn.no/lookup.html?finnkode="
dir_prj = "/home/tian/HDD1T/Finn/"

codeLen = 10000000
codeFirst = int(8 * codeLen)
codeLast  = int(8.8 * codeLen )

pag = dir_prj + "pages_8/" 
log = dir_prj + "log_8" 


codes_all = []
with open(log, "r") as f:
    for line in f:
        if line[9:10] != "O" and line[9:10] != "N":
            codes_all.append(int(line[0:8]))          
    f.close()

codes_downloaded = []
with open(log, "r") as f:
    for line in f:
        if line[9:10] == "O" or line[9:10] == "N":
            codes_downloaded.append(int(line[0:8]))
    f.close() 


## Codes plan to download;
codes = list(set(codes_all) - set(codes_downloaded)) 
print "There are " + str(len(codes)) + " codes need to redownload!"


