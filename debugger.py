from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from selenium.webdriver.support.ui import Select

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time 
import calendar 
from datetime import date
from selenium.webdriver.chrome.options import Options
def get_speech_imf():
    '''
    Scraps both the Transcripts and the Speech section of the IMF website. 
    '''
    #today = self.get_month()[0:3]

    url = r'https://www.imf.org/en/news/searchnews#sort=%40imfdate%20descending'

    # initialize an instance of the Chrome driver (browser) in headless mode    
    # instantiate Chrome WebDriver without headless mode
    driver = webdriver.Firefox()




    driver.implicitly_wait(15)
    # URL of the web page to scrape
    #url = "https://www.scrapingcourse.com/javascript-rendering"

    # open the specified URL in the browser
    driver.get(url)

    time.sleep(8)
    driver.find_elements(By.CLASS_NAME, 'CoveoResultList')
    driver.find_element(By.ID,'NewsType')
    driver.find_element(By.TAG_NAME,'option')




    time.sleep(5)
    #Goes to the speech sections and scraps the html there
    select_element = driver.find_element(By.ID,'NewsType')
    select = Select(select_element)


    print(select.options)

    select.select_by_value("Speech")
    pages_to_scrap = []

    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, 'html5lib')
    pages_to_scrap.append(soup)                


    #Goes to the transcripts sections and scraps the html there

    #select.select_by_value("Transcript")

    #soup_2 = BeautifulSoup(driver.page_source, 'html5lib')
    #pages_to_scrap.append(soup_2)    


    for page in pages_to_scrap:
        titles = page.find_all(class_ = 'CoveoResultLink')
        dates = page.find_all(class_ = 'CoveoFieldValue')

        for i,n in zip(titles, dates):
            print(i.string)
            print(n.span.string)


    driver.quit()
    final = []
    return final 


get_speech_imf()