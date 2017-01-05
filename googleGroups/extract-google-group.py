from bs4 import BeautifulSoup as BS
import time, re, os, pickle, sys

wd = "/home/tian/shinyExpert/"
path = wd + "topics/"
HTML = os.listdir(path)
HTML.sort()
topics = []

for i in range(0, len(HTML)):
    ## print f
    f = HTML[i]
    bs = BS(open(path + f).read())
    ## title
    try:
        title = bs.find("span", {"id": "t-t"}).get_text()
    except:
        title = ""
        print "\nWarning: file " + f + " has no title!"
    threads = [{"id": f,"title": title}]
    ## threads
    thread_items = bs.findAll("div", {"class": "IVILX2C-tb-x"})
    N = len(thread_items)
    if (N > 0):
        for n in range(0, N):
            try:
                author  = thread_items[n].find("table", {"class": "IVILX2C-tb-O"}).find("td", {"align": "left"}).get_text()
            except:
                author = ""
                print "\nWarning: index = " + str(i) + "; file " + f + " has no author!"
            try:
                td_date = thread_items[n].find("table", {"class": "IVILX2C-tb-O"}).find("td", {"align": "right"})
                date = td_date.find("span", {"class": "IVILX2C-tb-Q IVILX2C-b-Cb"})["title"]
            except:
                date = ""
                print "\nWarning: index = " + str(i) + "; file " + f + " has no date!"
            try:
                content = thread_items[n].find("div", {"class": "IVILX2C-tb-P"}).find("div", {"dir": "ltr"}).get_text()
            except:
                content = ""  
                print "\nWarning: index = " + str(i) + "; file " + f + " has no content!"
            thread = {"author": author, "date":date, "content":content}
            threads.append(thread)        
    else:
        with open(wd + 'log_extract.txt', "w") as log:
            log.write(f + "\n")
            log.close()
        print "\nError: file " + f + " wasn't downloaded completely!"
    topics.append(threads)
    msg = "\rProcessed " + str(i+1) + " files: " + f
    sys.stdout.write(msg); sys.stdout.flush()




dat_topics = wd + "topics.dat"
pickle.dump(topics, open(dat_topics, "wb"))
#topics = pickle.load(open(dat_topics, "r"))




"""
for f in HTML:
    t = os.path.getctime(path + f)
    d = datetime.datetime.fromtimestamp(t).strftime('%Y%m%d_%H%M%S_')
    os.rename(path + f, path + d + f)
    print path + d + f
"""  

