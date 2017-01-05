from pyvirtualdisplay import Display
from selenium import webdriver
from bs4 import BeautifulSoup as BS
import time, re, sys

## Note: include ?hl=en make sure the page display language is English, otherwise will be the system default language.
gg = 'https://groups.google.com/forum/?hl=en#!forum/shiny-discuss'
wd = "/home/tian/shinyExpert/"


display = Display(visible=0, size=(1920, 1080)).start()
browser = webdriver.Firefox()
browser.get(gg)
time.sleep(2)
print browser.title.encode('utf8', 'replace')

n = 0;
t0 = time.time(); 
topic_last = browser.find_elements_by_xpath("(//tbody/*//a[contains(@href, '#!topic')])[last()]")[0]
id1 = topic_last.get_attribute('id'); 
while True: 
    js = 'document.getElementById("' + id1 + '").focus()'
    browser.execute_script(js)
    time.sleep(2+n/100)
    t1 = time.time()
    topic_last = browser.find_elements_by_xpath("(//tbody/*//a[contains(@href, '#!topic')])[last()]")[0]
    id2 = topic_last.get_attribute('id')
    if (id1 != id2):
        n = n + 1
        id1 = id2
        msg = "\rLoad: " + str(n) + " times; Used seconds:" + str(round(time.time()- t1, 3))
        sys.stdout.write(msg);sys.stdout.flush()         
    else:
        time.sleep(2)
        topic_last = browser.find_elements_by_xpath("(//tbody/*//a[contains(@href, '#!topic')])[last()]")[0]
        id2 = topic_last.get_attribute('id')
        if (id1 != id2):
            n = n + 1
            id1 = id2
            print "\nReload! " + str(n) + " times; Used seconds:" + str(round(time.time()- t1, 3))         
        else:
            print "\nAll content loaded!"
            break

with open(wd + 'forum.html', "w") as f:
    f.write(browser.page_source.encode('utf8', 'replace'))
    f.close()

print '\nTotal scraping used: ' + str(round(time.time()- t0)) + ' seconds!'
N = len(browser.find_elements_by_xpath("//tbody/tr/*//a[contains(@href, '#!topic')]"))
print 'Total threads: ' + str(N)




bs = BS(open("/home/tian/shinyExpert/forum.html").read())                                                                 
HREF = bs.findAll("a", {"class": "IVILX2C-p-Q"}) 
N = len(HREF) 
                                                    
for n in range(0, N):
    if (n % 500 == 0):
        browser = webdriver.Firefox(); time.sleep(1)
        print '\nBrowser cache cleaned!'
    href = HREF[n].get('href')
    url  = re.sub('#!.*$', href, gg)      
    try:                                                                                                
        browser.get(url)                                                        
        time.sleep(2) 
        divs = browser.find_elements_by_xpath("//div[@class='IVILX2C-tb-x']")         
        if (len(divs) == 0):
            browser.get(url)
            time.sleep(10)
            divs = browser.find_elements_by_xpath("//div[@class='IVILX2C-tb-x']")
            print "\nLength of divs equal 0! After 10 seconds, length of divs equal: " + str(len(divs))
            if (len(divs) == 0):
                with open(wd + 'log_download.txt', "w") as log:
                    log.write(url + "\n")
                    log.close()
        else:
            time.sleep(1)
        ## file_name = time.strftime("%Y%m%d_%H%M%S_")
        file_name = '{:04d}'.format(n+1) + re.sub('^.*/', '_', href)
        with open(wd + 'topics/' + file_name, "wb") as f:
            f.write(browser.page_source.encode('utf8', 'replace'))
            f.close()
        msg = "\rIndex: " + str(n) + "; file: "+ file_name
        sys.stdout.write(msg); sys.stdout.flush()     
    except:
        print "\nBrowser fail to get: " + href


