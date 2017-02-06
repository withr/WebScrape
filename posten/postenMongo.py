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







URL = "http://eiendom.statkart.no/Search.ashx?filter=KILDE:sted,matreiendom,SITEURLKEY:httpwwwseeiendomno,LESEGRUPPER:guests&term="

proxies_ls = [
    "https://37.9.45.242:8085",
    "https://91.243.94.120:8085",
    "https://93.179.89.230:8085",
    "https://146.185.204.86:8085",
    "https://91.243.89.89:8085"] 


N = 0

def eiendom(id):
	add = address.find()[id]
	term = add['ADRESSE'] + ', ' + add['POSTNR']+ ' ' + re.sub(' *\t *', '', add['KOMMUNE'])
	url=URL+term
	proxy = {"https": proxies_ls[id % len(proxies_ls)]}
	r = requests.get(url, proxies = proxy, timeout=5)
	global N
	N = N + 1
	if r.content != '[]':
		address.update({'_id': add['_id']}, {'$set':{ 'eiendom': r.content.decode('latin-1')}}, upsert=True)
		msg = "\r " + str(N) + " processed!"
		sys.stdout.write(msg); sys.stdout.flush()




ID = range(0, address.count())


pool = Pool(8)
pool.map(eiendom, ID) 
pool.close()  
pool.join()  












