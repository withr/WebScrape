from pyvirtualdisplay import Display
from selenium import webdriver
from bs4 import BeautifulSoup as BS
import time, re, sys

## Note: include ?hl=en make sure the page display language is English, otherwise will be the system default language.
gg = 'https://w2.brreg.no/eHandelPortal/ecomsys/sok.jsp'


time_wait = 60
nrs = [840398412,971437286]
for i in range(160,len(nrs)): 
    print str(i) + ": " + str(nrs[i])
    ## Login
    if i % 10 == 0:
        display = Display(visible=0, size=(1920, 1080)).start()
        browser = webdriver.Firefox()
        browser.get(gg)
        time.sleep(10)
        print browser.title.encode('utf8', 'replace')
        login = browser.find_element_by_link_text('Logg inn')
        login.click()
        time.sleep(10)
        username = browser.find_element_by_name("username")
        password = browser.find_element_by_name("password")
        username.send_keys("tianhd.ioz@gmail.com")
        password.send_keys('Tian!"34')
        browser.find_element_by_name("Logginn").click()
        ## Tidligere bestillinger
        wait0 = True
        t0 = time.time()
        while wait0:
            time.sleep(2)
            try:
                bestil = browser.find_element_by_link_text('Tidligere bestillinger')
                bestil.click()
                time.sleep(10)
                wait0 = False
            except:
                pass
            if (time.time() - t0) > time_wait: wait0 = False
    ## enhetsnr
    searchUI = True
    t1 = time.time()
    while searchUI:
        time.sleep(2)
        try:
            enhetsnr = browser.find_element_by_name("enhetsnr")
            searchUI = False
        except:
            pass
        if (time.time() - t1) > time_wait: searchUI = False
    enhetsnr.send_keys(str(nrs[i]))
    browser.find_element_by_name("søk").click()
    ## 5040
    pdfUI = True
    t2 = time.time()
    while pdfUI:
        time.sleep(2)
        try:
            pdf = browser.find_element_by_name("5040")
            pdfUI = False
        except:
            pass
        if (time.time() - t2) > time_wait: searchUI = False
    try: 
        pdf = browser.find_element_by_name("5040")
        pdf.click()    
        time.sleep(10)
        submit = browser.find_element_by_name("Submit")
        submit.click()
        time.sleep(10)        
    except:
        time.sleep(10)
        submit = browser.find_element_by_name("Submit")
        submit.click()
        time.sleep(10)
    ## send request to server 
    if (i % 10 == 9) or (i == (len(nrs)-1)):
        ## Submit
        wait1 = True
        t1 = time.time()
        while wait1:
            time.sleep(2)
            try:
                Submit = browser.find_element_by_name("Submit")
                Submit.click()
                time.sleep(10)
                wait1 = False
            except:
                pass
            if (time.time() - t1) > time_wait: wait1 = False
        ## Submit
        wait2 = True
        t2 = time.time()
        while wait2:
            time.sleep(2)
            try:
                Submit = browser.find_element_by_name("Submit")
                Submit.click()
                time.sleep(10)
                wait2 = False
            except:
                pass
        if (time.time() - t2) > time_wait: wait2 = False
        ## log out
        wait3 = True
        t3 = time.time()
        while wait3:
            time.sleep(2)
            try:
                logut = browser.find_element_by_link_text('Logg ut')
                logut.click()
                time.sleep(10)
                print "send to server!"
                wait3 = False
            except:
                pass
            if (time.time() - t3) > time_wait: wait3 = False
