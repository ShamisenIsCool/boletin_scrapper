# pip3 install selenium
from bs4 import BeautifulSoup
from bs4 import SoupStrainer


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time 
import calendar 
from datetime import date


def get_month():
    return date.today().strftime("%B")


def scrap_link(): 

    today = date.today() 

    days_of_month = str(calendar.monthrange(today.year, today.month)[1])

    #test parameter
    date_parameter = f'&DateTo=12%2F{days_of_month}%2F{today.year - 1}&DateFrom=12%2F1%2F{today.year - 1}'

    #final parameter, uncommment when program is ready. Overrides previous parameter
    #date_parameter = f'&DateTo={today.month}%2F{days_of_month}%2F{today.year}&DateFrom={today.month}%2F1%2F{today.year}'


    print(date_parameter)





    url =r'https://www.imf.org/en/Publications/Search#sort=%40imfdate%20descending&numberOfResults=20&f:series=[WRKNGPPRS]'
    url = url + date_parameter

    # instantiate a Chrome options object
    options = webdriver.ChromeOptions()

    # set the options to use Chrome in headless mode
    options.add_argument("--headless=new")
    
    # initialize an instance of the Chrome driver (browser) in headless mode
    driver = webdriver.Chrome(options=options)
    # instantiate Chrome WebDriver without headless mode
    #driver = webdriver.Chrome()




    driver.implicitly_wait(25)
    # URL of the web page to scrape
    #url = "https://www.scrapingcourse.com/javascript-rendering"

    # open the specified URL in the browser
    driver.get(url)
    driver.find_elements(By.CLASS_NAME, "CoveoResultLink")
    driver.find_elements(By.TAG_NAME, 'h3')





    soup = BeautifulSoup(driver.page_source, 'html5lib')


    #def has_class_but_no_name(tag): 
    #    return tag.string != 'Download PDF' and tag.get('class',' ') == 'CoveoResultLink'

    l = soup.find_all(class_ = 'CoveoResultLink')
    k = [e for e in l if e.string != 'Download PDF']

    final = [] #Lista donde se agregara un tuple de dos elementos a cada indice de la lista. 
    for e in k:
        print((e.string))
        print(e['href'])
        pair = (e.string, e.get('href'))
        final.append(pair)
    
    

    #result = soup.find_all(has_class_but_no_name(soup.a))




    # print the page source
    '''
    for e in link:
        if e != 'Download PDF':
            print(e.text)
        else:
            continue
    # close the browser
    '''
    driver.quit()
    return final 


