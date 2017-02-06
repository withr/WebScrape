#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re, sys, os, time, subprocess
from bs4 import BeautifulSoup as BS
from pymongo import MongoClient
from multiprocessing.dummy import Pool


##connect to default MongoClient
client = MongoClient()
##client.drop_database('FinnBoligTilSalg')

## Link to a database, if the database not exist, create it.
db = client['FinnBoligTilSalg']
## create a collection (like a table)
collection = db['pages']
collection.count()


folder = "/home/tian/HDD1T/Finn/pages_7/Eiendom/Bolig\ til\ salgs"
shellMSG = subprocess.check_output("find " + folder + " -type f", shell=True)
html_ls =  shellMSG.split('\n')
len(html_ls)

def html2mongo(html): 
    finnkode = html[-13:-5]
    HTML= open(html).read()
    Item = {
        "_id"     : html[-13:-5],
        "length"  : len(HTML),
        "category": re.search("pages_.*?/(.*)/", html).group(1).split('/')
    }  
    try:
        bs = BS(HTML)
        ln = bs.find("div", {"class": "line"})
        bd = ln.find("div", {"class": "bd"})
        try:
            title = bd.h1.get_text()
            Item['title'] = title
        except:
            msg = finnkode + " Title missed!\n"
            print msg          
        try:
            address = bd.h1.find_next_sibling("p").get_text()
            Item['address'] = address
        except:
            msg = finnkode + " Address missed!\n"
            print msg 
        ## <div class='dl'>
        try:
            dls = bd.findAll("dl")
            for i in range(len(dls)):
                items = []
                dls_dt = dls[i].findAll("dt")
                dls_dd = dls[i].findAll("dd")
                for n in range(len(dls_dt)):
                    if dls_dt[n] is not None and  dls_dd[n] is not None:
                        key = re.sub(r"\n *", "", dls_dt[n].get_text())
                        val = re.sub(r"\n *", "", dls_dd[n].get_text())
                        dic = {re.sub(r"\.", "_", key): val}
                        items.append(dic)
                Item['dl'+str(i)] = items    
        except:
            msg = finnkode + " dls missed!\n"
            print msg  
        ## <div class='mbl'>
        try:
            mbls = bd.findAll("div", {"class": "mbl"})
            for i in range(len(mbls)):
                if mbls[i].h2 is not None and  mbls[i].p is not None:
                    key = re.sub(r"\n *", "", mbls[i].h2.get_text())
                    val = re.sub(r"\n *", "", mbls[i].p.get_text())
                    Item[re.sub(r"\.", "_", key)] = val
        except:
            msg = finnkode + " mbls missed!\n"
            print msg
        ## <div class='hide-lt768'>
        try:
            hides = bd.findAll("div", {"class": "hide-lt768"})
            hidps = hides[len(hides)-1].findAll("p")
            items = []
            for i in range(len(hidps))[1:-1]:
                if hidps[i] is not None:
                    txt = hidps[i].get_text().split(": ")
                    dic = {txt[0] : txt[1]}
                    items.append(dic)
            Item["Ref"] = items
        except:
            msg = finnkode + " hides missed!\n"
            print msg   
    except:
        msg = finnkode + " Parse failed!\n"
        print msg
    #return Item    
    collection.insert(Item)
    msg = "\rImported " + str(collection.count()) + " files!"
    sys.stdout.write(msg); sys.stdout.flush()  

t1 = time.time()
pool = Pool(8)
pool.map(html2mongo, html_ls) 
pool.close()  
pool.join()
print "\nImporting used " + str(int(time.time() - t1)) + " seconds in total!\n"


