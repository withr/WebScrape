#from pyvirtualdisplay import Display
from selenium import webdriver
#from bs4 import BeautifulSoup as BS
import time, re, sys

## Note: include ?hl=en make sure the page display language is English, otherwise will be the system default language.
gg = 'https://w2.brreg.no/eHandelPortal/ecomsys/sok.jsp'
time_wait = 90

## Login
print("webdriver.Firefox start ...")
#display = Display(visible=0, size=(1920, 1080)).start()
browser = webdriver.Firefox()
browser.get(gg)
time.sleep(2)
print(browser.title.encode('utf8', 'replace'))
login = browser.find_element_by_link_text('Logg inn')
login.click()
print("log in ...")
wait_log = True
t0 = time.time()
while wait_log:
    time.sleep(2)
    try:
        username = browser.find_element_by_name("username")
        password = browser.find_element_by_name("password")
        username.send_keys("tianhd.slu@gmail.com")
        password.send_keys('Tian!"34')
        browser.find_element_by_name("Logginn").click()
        wait_log = False
    except:
        pass
    if (time.time() - t0) > time_wait: 
        wait_log = False



nrs = [839627262,971437286]

for i in range(20,len(nrs)): 
    print(str(i) + ": " + str(nrs[i]))
    if i % 10 == 0:
        ## Tidligere bestillinger
        print("Tidligere bestillinger")
        wait0 = True
        t0 = time.time()
        while wait0:
            time.sleep(2)
            try:
                bestil = browser.find_element_by_link_text('Tidligere bestillinger')
                bestil.click()
                time.sleep(5)
                wait0 = False
            except:
                pass
            if (time.time() - t0) > time_wait: 
                wait0 = False    
    ## enhetsnr
    searchUI = True
    t1 = time.time()
    while searchUI:
        time.sleep(2)
        try:
            enhetsnr = browser.find_element_by_name("enhetsnr")
            print("found enhetsnr")
            searchUI = False
        except:
            pass
        if (time.time() - t1) > time_wait: 
            searchUI = False
    enhetsnr.send_keys(str(nrs[i]))
    print("try to find søk")
    browser.find_element_by_name("søk").click()
    ## Årsregnskap
    existSkap = True
    t2 = time.time()
    while existSkap:
        time.sleep(2)
        try:
            print("try to find Årsregnskap")
            skaps  = browser.find_elements_by_xpath("//td/p[contains(text(), 'Årsregnskap (kr 0/år) ')]/parent::td/following-sibling::td")
            print("found Årsregnskap")
            existSkap = False
            time.sleep(5)
            ## 2016
            try:
                print("try to find 2016")
                skaps = browser.find_elements_by_xpath("//td/p[contains(text(), 'Årsregnskap (kr 0/år) ')]/parent::td/following-sibling::td")
                skap1 = skaps[1].find_element_by_xpath("div/form/input[@type='checkbox']")
                if skap1.is_displayed():
                    skap1.click()
                    print("found skap                     2016")
                    time.sleep(5)
                else:
                    print("object is invisible for        2016")
            except:
                pass
            ## 2015
            try:
                print("try to find 2015")
                skaps = browser.find_elements_by_xpath("//td/p[contains(text(), 'Årsregnskap (kr 0/år) ')]/parent::td/following-sibling::td")
                skap2 = skaps[2].find_element_by_xpath("div/form/input[@type='checkbox']")
                if skap2.is_displayed():
                    skap2.click()
                    print("found skap                     2015")
                    time.sleep(5)
                else:
                    print("object is invisible for        2015")
            except:
                pass
        except:
            pass
        if (time.time() - t2) > time_wait: 
            existSkap = False
    print("Find submit button")
    submit1 = True
    t3 = time.time()
    while submit1:
        time.sleep(2)
        try:
            submit = browser.find_element_by_name("Submit")
            submit.click()
            submit1 = False
            print("Submitted to cart")
        except:
            pass
        if (time.time() - t3) > time_wait: 
            submit1 = False
    time.sleep(2)
    ## send request to server 
    if (i % 10 == 9) or (i == (len(nrs)-1)):
        ## Submit
        wait1 = True
        t1 = time.time()
        print("ready to submit order (1)")
        while wait1:
            time.sleep(2)
            try:
                Submit = browser.find_element_by_name("Submit")
                Submit.click()
                time.sleep(2)
                wait1 = False
            except:
                pass
            if (time.time() - t1) > time_wait: 
                wait1 = False
        ## Submit
        wait2 = True
        t2 = time.time()
        print("ready to submit order (2)")
        while wait2:
            time.sleep(2)
            try:
                Submit = browser.find_element_by_name("Submit")
                Submit.click()
                print "send to server!"
                time.sleep(2)
                wait2 = False
            except:
                pass
        if (time.time() - t2) > time_wait: 
            wait2 = False




