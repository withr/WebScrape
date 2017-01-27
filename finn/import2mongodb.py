#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re, sys, os, time, subprocess
from bs4 import BeautifulSoup as BS
from pymongo import MongoClient
from multiprocessing.dummy import Pool


##connect to default MongoClient
client = MongoClient()
## Link to a database, if the database not exist, create it.
db = client['mongoFinn']
## create a collection (like a table)
collection = db['HTMLs']



shellMSG = subprocess.check_output("find /home/tian/HDD1T/Finn/pages_8 -type f", shell=True)
html_ls =  shellMSG.split('\n')


def html2mongo(html):
    item = {
        "_id"  : html[-13:-5],
        "category"  : re.search("pages_.*?/(.*)/", html).group(1).split('/'),
        "bs"        : open(html).read()
    }
    collection.insert(item)
    msg = "\rImported " + str(collection.count()) + " files!"
    sys.stdout.write(msg); sys.stdout.flush()  

t1 = time.time()

pool = Pool(16)
pool.map(html2mongo, html_ls) 
pool.close()  
pool.join()

print "\nImporting used " + str(int(time.time() - t1)) + " seconds in total!\n"






        
