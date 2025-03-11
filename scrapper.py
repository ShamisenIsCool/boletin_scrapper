from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time 
import calendar 
from datetime import date
from selenium.webdriver.support.ui import Select
from selenium_stealth import stealth



#final equals a list of tuples, each tuples equals a pair, each pair consists of a title (first) and a link (second)

class Scrapper:
    '''
    Objeto que recupera links de diferentes paginas web de acuerdo a el mes, por default el mes se fija a el mes en curso.  
    '''    

    def __init__(self, links_list = [], month =[]):
        
        today = date.today() 

        #self.links_list = links_list
        #self.month = month 

        self.websites = list()
        self.wn = list()



    def get_webnames(self):
        return self.wn

    def get_all_websites(self):
        '''
        Returns a list of lists. These lists contains tuples of pairs. Each pair consists of a title and a link. 
        '''
        return self.websites

    def get_month(self):
        return date.today().strftime("%B")

    def access_imf(self, url):
        '''
        Función que recupera links de working papers del IMF de acuerdo a el mes, por default el mes se fija a el mes en curso.  
        '''
        #month = self.month  
        #links = self.links_list

        today = date.today() 

        days_of_month = str(calendar.monthrange(today.year, today.month)[1])

        #test parameter
        date_parameter = f'&DateTo=12%2F{days_of_month}%2F{today.year - 1}&DateFrom=12%2F1%2F{today.year - 1}'

        #final parameter, uncommment when program is ready. Overrides previous parameter
        date_parameter = f'&DateTo={today.month}%2F{days_of_month}%2F{today.year}&DateFrom={today.month}%2F1%2F{today.year}'

        print(date_parameter)
        url =r'https://www.imf.org/en/Publications/Search#sort=%40imfdate%20descending&numberOfResults=50&f:series=[WRKNGPPRS]'
        url = url + date_parameter

        # instantiate a Chrome options object
        options = webdriver.ChromeOptions()

        # set the options to use Chrome in headless mode
        options.add_argument("--headless=new")
        
        # initialize an instance of the Chrome driver (browser) in headless mode
        driver = webdriver.Chrome(options=options)
        # instantiate Chrome WebDriver without headless mode
        #driver = webdriver.Chrome()




        driver.implicitly_wait(20)
        # URL of the web page to scrape
        #url = "https://www.scrapingcourse.com/javascript-rendering"

        # open the specified URL in the browser
        driver.get(url)
        driver.find_elements(By.CLASS_NAME, "CoveoResultLink")
        driver.find_elements(By.TAG_NAME, 'h3')
        driver.find_elements(By.TAG_NAME, 'a')
        
        soup = BeautifulSoup(driver.page_source, 'html5lib')

        #def has_class_but_no_name(tag): 
        #    return tag.string != 'Download PDF' and tag.get('class',' ') == 'CoveoResultLink'

        l = soup.find_all(class_ = 'CoveoResultLink')
        k = [e for e in l if e.string != 'Download PDF']

        final = [] #Lista donde se agregara un tuple de dos elementos a cada indice de la lista. 
        for e in k:
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
        final.reverse()
        


        self.websites.append(final)
        driver.quit()
        return final

    
    def get_imf_reports(self): 
        
        url = r'https://www.imf.org/en/Search#sort=relevancy&numberOfResults=20&f:type=[PUBS,COUNTRYREPS,ARTICLE4]'

        return self.access_imf(url)

    def get_imf_wp(self):
        url = r'https://www.imf.org/en/Publications/Search#sort=%40imfdate%20descending&numberOfResults=50&f:series=[WRKNGPPRS]'
        self.wn.append('IMF - Working Papers.')
        return self.access_imf(url)



    def get_speech_bis(self): 
        today = self.get_month()[0:3]


        url = r'https://www.bis.org/cbspeeches/index.htm?cbspeeches_page_length=25'
        url2 = r'https://www.bis.org/cbspeeches/index.htm?cbspeeches_page=2&cbspeeches_page_length=25'
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
        driver.find_elements(By.TAG_NAME, 'p')
        driver.find_elements(By.TAG_NAME, 'tr')

        time.sleep(8) #waits 15 seconds for page to load 

        pages_to_scrap = []
        soup = BeautifulSoup(driver.page_source, 'html5lib')
        pages_to_scrap.append(soup)        

        move_next_page = driver.find_element(By.CLASS_NAME, 'icon-chevron-right')
        move_next_page.click()

        soup_2 = BeautifulSoup(driver.page_source, 'html5lib')
        pages_to_scrap.append(soup_2)

        final = []
        for page in pages_to_scrap:

            #every page is a soup object (from the BeautifulSoup Library)
            titles = page.find_all(class_ = 'title')
            dates = page.find_all(class_ = 'item_date')

            for i,n in zip(titles, dates):
                if today.lower() in n.string.lower(): 
                    link = r'https://www.bis.org' + i.a.get('href')
                    text = i.a.span.string + i.a.span.next_sibling.string
                    pair = (text, link)
                    final.append(pair)

        
        final.reverse()

        self.wn.append('BIS - Speeches')
        self.websites.append(final)
        driver.quit()
        return final
    
    def get_speech_imf(self):
        '''
        Scraps both the Transcripts and the Speech section of the IMF website. 
        '''
        today = self.get_month()[0:3]


        url = r'https://www.imf.org/en/news/searchnews#sort=%40imfdate%20descending'

        options = webdriver.ChromeOptions()

        # set the options to use Chrome in headless mode
        options.add_argument("--headless=new")

        
        # initialize an instance of the Chrome driver (browser) in headless mode
        driver = webdriver.Chrome(options=options)
        # instantiate Chrome WebDriver without headless mode
        #driver = webdriver.Chrome()




        driver.implicitly_wait(15)
        # URL of the web page to scrape
        #url = "https://www.scrapingcourse.com/javascript-rendering"

        # open the specified URL in the browser
        driver.get(url)
        driver.find_elements(By.CLASS_NAME, 'CoveoResultList')
        driver.find_element(By.ID,'NewsType')
        driver.find_element(By.TAG_NAME,'option')




        time.sleep(3)
        #Goes to the speech sections and scraps the html there
        select_element_f = driver.find_element(By.CLASS_NAME,'coveo-custom-dropdown-search')
        select_element = select_element_f.find_element(By.TAG_NAME, 'select')
        select = Select(select_element)

        filter = driver.find_element(By.CLASS_NAME, 'coveo-custom-filter-button')

        #print(select.options)

        select.select_by_value("Speech")
        filter.click()

        pages_to_scrap = []

        time.sleep(4)

        soup = BeautifulSoup(driver.page_source, 'html5lib')
        pages_to_scrap.append(soup)                


        #Goes to the transcripts sections and scraps the html there

        select.select_by_value("Transcript")
        filter.click()
        time.sleep(4)
        soup_2 = BeautifulSoup(driver.page_source, 'html5lib')
        pages_to_scrap.append(soup_2)    

        final = []
        for page in pages_to_scrap:
            titles = page.find_all('a', class_ = 'CoveoResultLink')
            dates = page.find_all(class_ = 'CoveoFieldValue')

            for i,n in zip(titles, dates):
                if n.span.string[0:3] == today:
                    text = i.string
                    link = i.get('href')
                    pair = (text, link)
                    final.append(pair)

        
        final.reverse()

        self.wn.append('IMF - Speeches and Transcripts')
        self.websites.append(final)
        driver.quit()
        return final 

    def get_fem_reports(self): 
        
        
        today = self.get_month()[0:3] #Gets current month 


        # instantiate Chrome WebDriver without headless mode
        #driver = webdriver.Chrome()

        #driver.implicitly_wait(15)
        # URL of the web page to scrape
        #url = "https://www.scrapingcourse.com/javascript-rendering"

        # open the specified URL in the browser


        final = []
        #Inicio de Loop. extrae el html desde la pagina 1 hasta la 4. Si la fecha no coincide con la de hoy, se finaliza el proceso de extracción. 
        for page in range(1,5):

            options = webdriver.ChromeOptions()

        # set the options to use Chrome in headless mode
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
        # initialize an instance of the Chrome driver (browser) in headless mode
            driver = webdriver.Chrome(options=options)
            driver.implicitly_wait(15)

            number_page = page
            url = f'https://www.weforum.org/publications/?types=Whitepaper%2CReport&page={number_page}'


            try: 
                driver.get(url)
            except: 
                try:
                    driver.quit()
                    driver = webdriver.Chrome(options=options)
                    driver.implicitly_wait(15)
                except:
                    return final
                
            print('Success')
            #Time the drivers wait for the website to load
            driver.find_elements(By.CLASS_NAME, 'chakra-link wef-spn4bz') #Searches element by class name, extracts LINK
            driver.find_elements(By.CLASS_NAME, 'chakra-text wef-usrq6c') #Extracts time of the element 
            time.sleep(3)
            soup = BeautifulSoup(driver.page_source, 'html5lib')

            results = soup.find('div', id = 'results')
            titles = results.find_all('a', class_='chakra-link wef-spn4bz') #list
            dates = results.find_all('time', class_ = 'chakra-text wef-usrq6c') #list

            
            for i,n in zip(titles,dates):
                if n.string[0:3].lower() != today.lower() and 'hour' not in n.string: #Here it filters the date, if n(which is the first three words of the month) equals today (which gets the current month) then: 
                    final.reverse()
                    self.wn.append('FEM (WEF) - White papers reports')
                    self.websites.append(final)
                    driver.quit()
                    return final 
                

                text= i.string

                link = i.get('href')
                pair = (text,link)
                final.append(pair)
                print(text)

                   
    def get_oecd_reports(self): 
        options = webdriver.ChromeOptions()

        # set the options to use Chrome in headless mode
        options.add_argument("--headless=new")
        options.add_argument("--enable-javascript")

        # initialize an instance of the Chrome driver (browser) in headless mode
        driver = webdriver.Chrome(options=options)

        #makes the scrapper more stealthy in order to bypass Cloudfare false flagging 
        stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )
        driver.implicitly_wait(10)

        url = r'https://www.oecd.org/en/search/publications.html?orderBy=mostRecent&page=0&facetTags=oecd-content-types%3Apublications%2Freports%2Coecd-languages%3Aen&minPublicationYear=2024&maxPublicationYear=2025'
        driver.get(url)
  
        e = driver.find_element(By.CLASS_NAME, 'cmp-pagination__next')        
        driver.find_elements(By.CLASS_NAME, 'search-result-list-item__title')
        driver.find_elements(By.CLASS_NAME, 'search-result-list-item__date')

        pages_to_scrap = []

        for i in range(0,2): 
            soup = BeautifulSoup(driver.page_source, 'html5lib')
            pages_to_scrap.append(soup)        
            driver.execute_script("arguments[0].scrollIntoView();", e) #scrolls down to the element, so selenium can click it
            time.sleep(2) #time to actually scroll down
            e.click()
            time.sleep(2)
            e = driver.find_element(By.CLASS_NAME, 'cmp-pagination__next') 


            


        for page in pages_to_scrap: 
            titles = page.find_all('div', class_ = 'search-result-list-item__title')
            dates = page.find_all('span', class_ = 'search-result-list-item__date')            
            
            for title, date in zip(titles, dates):
                print(date.string.strip())
                print(title.a.string)
                print(title.a['href'])
                
     



if __name__ == '__main__':
    h = Scrapper()
    h.get_oecd_reports()
