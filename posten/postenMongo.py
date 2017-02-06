#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re, sys, os, random, time, requests
from bs4 import BeautifulSoup as BS
from pymongo import MongoClient


##connect to default MongoClient
client = MongoClient()
## Link to a database, if the database not exist, create it.
db = client['posten']


dir_html = "/home/tian/Posten/"

## create a collection (like a table)
postnrs = db['postnrs']
pages = dir_html + "pages/"
HTML = os.listdir(pages)
HTML.sort()

for i in range(0, len(HTML)):
    ## print f
    html = pages + HTML[i]
    post = {
        "postnr": HTML[i][0:4],
        "source": open(html).read()  
    }
    postnrs.insert(post)

#############
log = db['log']
f = open(dir_html + 'log', 'r')
for line in f:
    parts = line.split(' ')
    item = {
        "postnr": parts[0],
        "exist" : parts[1]
    }
    log.insert(item)



###########
postnrsValid = []
log_all = log.find()
for i in range(log_all.count()):
    log_one = log_all[i]
    if log_one['exist'] == "OK":
        postnrsValid.append(log_one['postnr'])

item = {"postnrsValid": postnrsValid}       
log.insert(item)   


##############
postnrs_all = postnrs.find()
address = db['address']
for post in postnrs_all:
    print post["postnr"]
    html = post["source"]
    bs = BS(html)
    tr_ls = bs.find_all('tr', {'class': 'result'})
    for tr in tr_ls:
        tr_str = tr.get_text().encode('utf8', 'replace').split('\n')
        add = tr_str[2]
        pst = tr_str[3]
        std = tr_str[4]
        kmn = tr_str[6]
        fyl = tr_str[8]
        ful = add + " " + pst + " " + std + " " + kmn + " " + fyl
        item = {
            "POSTNR":post["postnr"],
            "ADRESSE":add,
            "POSTNR":pst,
            "POSTSTED":std,
            "KOMMUNE":kmn,
            "FYLKE":fyl,
            "FULLADRESSE":ful
        }
        address.insert(item)














