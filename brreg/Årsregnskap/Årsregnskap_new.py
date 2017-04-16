from selenium import webdriver
import time, re, sys

## Login
print("webdriver.Firefox start ...")
#display = Display(visible=0, size=(1920, 1080)).start()
browser = webdriver.Firefox()
browser.implicitly_wait(20)
browser.get('https://w2.brreg.no/eHandelPortal/ecomsys/sok.jsp')
print(browser.title.encode('utf8', 'replace'))
login = browser.find_element_by_link_text('Logg inn')
login.click()
print("log in ...")
username = browser.find_element_by_name("username")
password = browser.find_element_by_name("password")
username.send_keys("tianhd.slu@gmail.com")
password.send_keys('Tian!"34')
browser.find_element_by_name("Logginn").click()
# get_attribute("innerHTML")

nrs = [839627262,971437286]

for i in range(10,len(nrs)): 
    print(str(i) + ": " + str(nrs[i]))
    if i % 10 == 0:
        print("Locate element: Tidligere bestillinger")
        bestil = browser.find_element_by_link_text('Tidligere bestillinger').click()
    print("Locate element: 'enhetsnr' input box")
    browser.find_element_by_name("enhetsnr").send_keys(str(nrs[i]))
    browser.find_element_by_xpath("//input[@value='Søk etter produkter']").click()
    print("Search button clicked")
    ## Årsregnskap
    try:
        print("Locate element: Årsregnskap")
        skaps  = browser.find_elements_by_xpath("//td/p[contains(text(), 'Årsregnskap (kr 0/år) ')]/parent::td/following-sibling::td//input[@type='checkbox']")
        print("Found Årsregnskap")
        if len(skaps) > 0:
            n0 = len(skaps[0].find_elements_by_xpath("../../../preceding-sibling::td"))
            if (n0 == 2) or (n0 == 3):
                if skaps[0].is_displayed():
                    skaps[0].click()
                    print("First checkbox selected!")
            skaps  = browser.find_elements_by_xpath("//td/p[contains(text(), 'Årsregnskap (kr 0/år) ')]/parent::td/following-sibling::td//input[@type='checkbox']")
            if len(skaps) > 1:
                n1 = len(skaps[1].find_elements_by_xpath("../../../preceding-sibling::td"))
                if n1 == 3:
                    if skaps[1].is_displayed():
                        skaps[1].click()
                        print("Second checkbox selected!")
    except:
        pass
    print("Locate element: Gå videre ->")
    submit = browser.find_element_by_name("Submit")
    submit.click()
    time.sleep(5)
    print("Submitted to cart")
    if (i % 10 == 9) or (i == (len(nrs)-1)):
        print("Locate element: 'Gå videre ->' for 'valgt følgende produkter'")
        Submit = browser.find_element_by_name("Submit").click()
        print("Locate element: 'Gå videre ->' for 'Aksepter og gå videre ->'")
        Submit = browser.find_element_by_xpath("//input[@value='Aksepter og gå videre ->']").click()
        time.sleep(5)
        print "Send order to server!"

