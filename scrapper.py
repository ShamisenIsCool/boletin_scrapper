from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time 
import calendar 
from datetime import date
from selenium.webdriver.support.ui import Select
import requests #to scrap websites who do not need javascript to scrap their html 
from selenium_stealth import stealth

#final equals a list of tuples, each tuples equals a pair, each pair consists of a title (first) and a link (second)
#All BIS websites' functions should flag these options to properly adress speed related issues observed when accesing a BIS website.
#options.add_argument("--disable-gpu") # Disables hardware acceleration through the GPU (Graphics Processing Unit). This can help avoid certain rendering issues and crashes, especially in headless mode or virtualized environments.
#options.add_argument("--no-sandbox") #  Disables Chrome's sandbox security feature. This speeds things up but reduces security isolation - generally only recommended in controlled environments like testing servers.
#options.add_argument("--disable-extensions") # Prevents Chrome extensions from loading, which saves memory and speeds up the browser's startup time.
#options.add_argument("--disable-dev-shm-usage") #Chrome uses shared memory (/dev/shm) for browser processes. This flag disables that usage, which helps prevent crashes in environments with limited memory like Docker containers. 

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
        #date_parameter = f'&DateTo=12%2F{days_of_month}%2F{today.year - 1}&DateFrom=12%2F1%2F{today.year - 1}'

        #final parameter, uncommment when program is ready. Overrides previous parameter
        date_parameter = f'&DateTo={today.month}%2F{days_of_month}%2F{today.year}&DateFrom={today.month}%2F1%2F{today.year}'

        print(date_parameter)
        #url =r'https://www.imf.org/en/Publications/Search#sort=%40imfdate%20descending&numberOfResults=50&f:series=[WRKNGPPRS]'
        url = url
        url = url + date_parameter

        # instantiate a Chrome options object
        options = webdriver.ChromeOptions()

        # set the options to use Chrome in headless mode
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu") # Disables hardware acceleration through the GPU (Graphics Processing Unit). This can help avoid certain rendering issues and crashes, especially in headless mode or virtualized environments.
        options.add_argument("--no-sandbox") #  Disables Chrome's sandbox security feature. This speeds things up but reduces security isolation - generally only recommended in controlled environments like testing servers.
        options.add_argument("--disable-extensions") # Prevents Chrome extensions from loading, which saves memory and speeds up the browser's startup time.
        options.add_argument("--disable-dev-shm-usage") #Chrome uses shared memory (/dev/shm) for browser processes. This flag disables that usage, which helps prevent crashes in environments with limited memory like Docker containers.        
        
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
        #driver.quit()
        return final

    
    def get_imf_reports(self): 
        
        url = r'https://www.imf.org/en/Search#sort=relevancy&numberOfResults=20&f:type=[PUBS,COUNTRYREPS,ARTICLE4]'
        self.wn.append('IMF - Reports.')
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
        options.add_argument("--disable-gpu") # Disables hardware acceleration through the GPU (Graphics Processing Unit). This can help avoid certain rendering issues and crashes, especially in headless mode or virtualized environments.
        options.add_argument("--no-sandbox") #  Disables Chrome's sandbox security feature. This speeds things up but reduces security isolation - generally only recommended in controlled environments like testing servers.
        options.add_argument("--disable-extensions") # Prevents Chrome extensions from loading, which saves memory and speeds up the browser's startup time.
        options.add_argument("--disable-dev-shm-usage") #Chrome uses shared memory (/dev/shm) for browser processes. This flag disables that usage, which helps prevent crashes in environments with limited memory like Docker containers.
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
        pages_to_scrap = []
        driver.get(url)
        driver.find_elements(By.TAG_NAME, 'p')
        driver.find_elements(By.TAG_NAME, 'tr')
        driver.find_element(By.CLASS_NAME, 'documentList')
        driver.find_element(By.CLASS_NAME, 'title')

        time.sleep(5) #waits 15 seconds for page to load 

        move_next_page = driver.find_element(By.CLASS_NAME, 'icon-chevron-right')
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)") #Scroll to the bottom
        #driver.execute_script("arguments[0].scrollIntoView();", move_next_page)

        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, 'html5lib')
        #print(soup.find('table', class_ = 'documentList'))
        pages_to_scrap.append(soup)        


        move_next_page.click()

        time.sleep(5)

        soup_2 = BeautifulSoup(driver.page_source, 'html5lib')
        #print('Second Soup')
        #print(soup_2.find('table', class_ = 'documentList'))
        pages_to_scrap.append(soup_2)

        final = []
        for page in pages_to_scrap:
            
            #every page is a soup object (from the BeautifulSoup Library)
            titles = page.find_all('div', class_ = 'title')
            dates = page.find_all('td', class_ = 'item_date')
            for i,n in zip(titles, dates):
                #print(i.a.span.string + i.a.span.next_sibling.string,n)
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

        options.add_argument("--disable-gpu") # Disables hardware acceleration through the GPU (Graphics Processing Unit). This can help avoid certain rendering issues and crashes, especially in headless mode or virtualized environments.
        options.add_argument("--no-sandbox") #  Disables Chrome's sandbox security feature. This speeds things up but reduces security isolation - generally only recommended in controlled environments like testing servers.
        options.add_argument("--disable-extensions") # Prevents Chrome extensions from loading, which saves memory and speeds up the browser's startup time.
        options.add_argument("--disable-dev-shm-usage") #Chrome uses shared memory (/dev/shm) for browser processes. This flag disables that usage, which helps prevent crashes in environments with limited memory like Docker containers.


        
        # initialize an instance of the Chrome driver (browser) in headless mode
        driver = webdriver.Chrome(options=options)
        # instantiate Chrome WebDriver without headless mode
        #driver = webdriver.Chrome()




        driver.implicitly_wait(20)
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

        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, 'html5lib')
        pages_to_scrap.append(soup)                


        #Goes to the transcripts sections and scraps the html there

        select.select_by_value("Transcript")
        filter.click()
        time.sleep(5)
        soup_2 = BeautifulSoup(driver.page_source, 'html5lib')
        pages_to_scrap.append(soup_2)    

        final = []
        for page in pages_to_scrap:
            titles = page.find_all('a', class_ = 'CoveoResultLink')
            dates = page.find_all(class_ = 'CoveoFieldValue')
            dates = [date for date in dates if date is not None]

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
            options.add_argument("--disable-gpu") # Disables hardware acceleration through the GPU (Graphics Processing Unit). This can help avoid certain rendering issues and crashes, especially in headless mode or virtualized environments.
            options.add_argument("--no-sandbox") #  Disables Chrome's sandbox security feature. This speeds things up but reduces security isolation - generally only recommended in controlled environments like testing servers.
            options.add_argument("--disable-extensions") # Prevents Chrome extensions from loading, which saves memory and speeds up the browser's startup time.
            options.add_argument("--disable-dev-shm-usage") #Chrome uses shared memory (/dev/shm) for browser processes. This flag disables that usage, which helps prevent crashes in environments with limited memory like Docker containers.


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
                
            #print('Success')
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

                #print(text)

            final.reverse()
            #self.wn.append('FEM - Reports')
            #self.websites.append(final)

                   
    def get_oecd_reports(self): 
        today = self.get_month()[0:3]
        final = []
        options = webdriver.ChromeOptions()

        # set the options to use Chrome in headless mode
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu") # Disables hardware acceleration through the GPU (Graphics Processing Unit). This can help avoid certain rendering issues and crashes, especially in headless mode or virtualized environments.
        options.add_argument("--no-sandbox") #  Disables Chrome's sandbox security feature. This speeds things up but reduces security isolation - generally only recommended in controlled environments like testing servers.
        options.add_argument("--disable-extensions") # Prevents Chrome extensions from loading, which saves memory and speeds up the browser's startup time.
        options.add_argument("--disable-dev-shm-usage") #Chrome uses shared memory (/dev/shm) for browser processes. This flag disables that usage, which helps prevent crashes in environments with limited memory like Docker containers.


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
        

        url = r'https://www.oecd.org/en/search/publications.html?orderBy=mostRecent&page=0&facetTags=oecd-content-types%3Apublications%2Freports%2Coecd-languages%3Aen&minPublicationYear=2024&maxPublicationYear=2025'
        driver.get(url)
        driver.implicitly_wait(20)
            
        driver.find_elements(By.CLASS_NAME, 'search-result-list-item__title')
        dates_b = driver.find_elements(By.CLASS_NAME, 'search-result-list-item__date')

        pages_to_scrap = []
        driver.execute_script("window.scrollTo(0, (document.body.scrollHeight/2))") #scrolls to the bottom of the page
        time.sleep(5)
        e = driver.find_element(By.CSS_SELECTOR, '[rel="next"]')

        #for date in dates_b:
        #    print(date.text)

        a = True
        first_page = True #the process will not stop unless the first page has already been recovered. 
        #Next month's reports are published early so as to stop this from prematurely stopping the scrapping process, this variable is created with the end of being used
        #by the condition to check whether to stop the loop. 
        while a: 
            for date in dates_b:
                if today not in date.text and not first_page:
                    a = False
            soup = BeautifulSoup(driver.page_source, 'html5lib')
            pages_to_scrap.append(soup)        
            driver.execute_script("arguments[0].scrollIntoView();", e) #scrolls down to the element, so selenium can click it
            time.sleep(2) #time to actually scroll down
            e.click()
            time.sleep(2)
            e = driver.find_element(By.CSS_SELECTOR, '[rel="next"]') 
            dates_b = driver.find_elements(By.CLASS_NAME, 'search-result-list-item__date')
            first_page = False 

        for page in pages_to_scrap: 
            titles = page.find_all('div', class_ = 'search-result-list-item__title')
            dates = page.find_all('span', class_ = 'search-result-list-item__date')            
            
            for title, date in zip(titles, dates):
                if today in date.string: 

                    text, link = title.a.string, title.a['href']
                    #print(text, link)
                    final.append((text,link))



        final.reverse()
        self.wn.append('OECD - Reports')
        self.websites.append(final)
                
    def get_bid_workingpapers(self): 

        today = self.get_month()
        final = []

        options = webdriver.ChromeOptions()
        # set the options to use Chrome in headless mode
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu") # Disables hardware acceleration through the GPU (Graphics Processing Unit). This can help avoid certain rendering issues and crashes, especially in headless mode or virtualized environments.
        options.add_argument("--no-sandbox") #  Disables Chrome's sandbox security feature. This speeds things up but reduces security isolation - generally only recommended in controlled environments like testing servers.
        options.add_argument("--disable-extensions") # Prevents Chrome extensions from loading, which saves memory and speeds up the browser's startup time.
        options.add_argument("--disable-dev-shm-usage") #Chrome uses shared memory (/dev/shm) for browser processes. This flag disables that usage, which helps prevent crashes in environments with limited memory like Docker containers.

        driver = webdriver.Chrome(options=options)
        url = r'https://publications.iadb.org/en?f%5B0%5D=type%3A4633'

        #Activates a stealth mode in order to bypass cloudfare protecctions. It is important to note that scrapping is allowed by the website so no rule is being infringed. 
        stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True)
        
        driver.get(url)
        driver.implicitly_wait(6)
        driver.find_elements(By.CLASS_NAME, 'views-field-field-title')

        soup = BeautifulSoup(driver.page_source, 'html5lib')
        t = soup.find_all('div', class_ ='views-field-field-title')
        d = soup.find_all('div', class_ = 'views-field-field-date-issued-text')

        titles =  [title.span.a for title in t if t is not None and title.span is not None] #Returns <a> tags 
        dates = [date.span for date in d if d is not None]#Returns <span> tag which contains month and year 

        for title, date in zip(titles, dates):
            if today[0:3] in date.string:
                title, link =  title.string, 'https://publications.iadb.org' + str(title['href'])
                final.append((title, link))
                #print(title)
                #print(link)
            else:
                break
        

        final.reverse()
        self.wn.append('BID - Working Papers')
        self.websites.append(final)
        #print('Success')
        return final 

    def get_speech_fsb(self):
        #Here we use the requests method to scrap the fsb website, since javascript is not needed to showing the content we are looking for and it is also faster.  
        today = self.get_month() #Gets name of running month 

        url = 'https://www.fsb.org/press/speeches-and-statements/'
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html5lib')

        titles = soup.find_all('div', class_ = 'post-title')

        main_container = soup.find('div', class_ = 'wp-bootstrap-blocks-row') #it gets main container
        main_container = main_container.find('div', class_ = 'display-posts-listing') #then it filters for child container where we want to extract dates from 
        dates = main_container.find_all('div', class_ = 'post-date')

        titles = [title.h3.a for title in titles if title.h3 is not None]
        dates = [date.span for date in dates]

        final =[]
        for title, date in zip(titles,dates): 
            if today in date.string: 
                title, link = title.string, title['href']
                final.append((title, link))
            else:
                break 
        final.reverse()
        self.wn.append('FSB - Speeches')
        self.websites.append(final)

        return final 
            
    def get_basel_speeches(self): 

        today = self.get_month()[0:3] #Gets current month 


        url = r'https://www.bis.org/bcbs_speeches/index.htm?m=258&doclist1_page_length=25'
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-gpu") # Disables hardware acceleration through the GPU (Graphics Processing Unit). This can help avoid certain rendering issues and crashes, especially in headless mode or virtualized environments.
        options.add_argument("--no-sandbox") #  Disables Chrome's sandbox security feature. This speeds things up but reduces security isolation - generally only recommended in controlled environments like testing servers.
        options.add_argument("--disable-extensions") # Prevents Chrome extensions from loading, which saves memory and speeds up the browser's startup time.
        options.add_argument("--disable-dev-shm-usage") #Chrome uses shared memory (/dev/shm) for browser processes. This flag disables that usage, which helps prevent crashes in environments with limited memory like Docker containers.
        # set the options to use Chrome in headless mode
        options.add_argument("--headless=new")

        # initialize an instance of the Chrome driver (browser) in headless mode
        driver = webdriver.Chrome(options=options)
        # instantiate Chrome WebDriver without headless mode
        #driver = webdriver.Chrome()




        driver.implicitly_wait(10)
        # URL of the web page to scrape
        #url = "https://www.scrapingcourse.com/javascript-rendering"

        # open the specified URL in the browser
        driver.get(url)
        driver.find_elements(By.TAG_NAME, 'p')
        driver.find_elements(By.TAG_NAME, 'tr')

        time.sleep(3) #waits 15 seconds for page to load 


        soup = BeautifulSoup(driver.page_source, 'html5lib')



        titles = soup.find_all(class_ = 'title')
        dates = soup.find_all(class_ = 'item_date')
        
        
        #i = tile
        #n = date
        final = [] 
        #print(titles)
        for i,n in zip(titles, dates):

            if today.lower() in n.string.lower(): 
                link = r'https://www.bis.org' + i.a['href']
                text = i.a.span.string + i.a.span.next_sibling.string
                pair = (text, link)
                #print(pair)
                final.append(pair)
            else:
                break 


        final.reverse()

        self.wn.append('BIS - Basel Speeches')
        self.websites.append(final)
        driver.quit()
        return final        
    def get_bisManagement_speeches(self): 

        today = self.get_month()[0:3] #Gets current month 


        url = r'https://www.bis.org/mgmtspeeches/index.htm?m=253&mgmtspeeches_page_length=25'
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-gpu") # Disables hardware acceleration through the GPU (Graphics Processing Unit). This can help avoid certain rendering issues and crashes, especially in headless mode or virtualized environments.
        options.add_argument("--no-sandbox") #  Disables Chrome's sandbox security feature. This speeds things up but reduces security isolation - generally only recommended in controlled environments like testing servers.
        options.add_argument("--disable-extensions") # Prevents Chrome extensions from loading, which saves memory and speeds up the browser's startup time.
        options.add_argument("--disable-dev-shm-usage") #Chrome uses shared memory (/dev/shm) for browser processes. This flag disables that usage, which helps prevent crashes in environments with limited memory like Docker containers.
        # set the options to use Chrome in headless mode
        options.add_argument("--headless=new")

        # initialize an instance of the Chrome driver (browser) in headless mode
        driver = webdriver.Chrome(options=options)
        # instantiate Chrome WebDriver without headless mode
        #driver = webdriver.Chrome()




        driver.implicitly_wait(10)
        # URL of the web page to scrape
        #url = "https://www.scrapingcourse.com/javascript-rendering"

        # open the specified URL in the browser
        driver.get(url)
        driver.find_elements(By.TAG_NAME, 'p')
        driver.find_elements(By.TAG_NAME, 'tr')

        time.sleep(3) #waits 15 seconds for page to load 


        soup = BeautifulSoup(driver.page_source, 'html5lib')



        titles = soup.find_all(class_ = 'title')
        dates = soup.find_all(class_ = 'item_date')
        
        
        #i = tile
        #n = date
        final = [] 
        for i,n in zip(titles, dates):

            if today.lower() in n.string.lower(): 
                link = r'https://www.bis.org' + i.a['href']
                text = i.a.span.string + i.a.span.next_sibling.string
                pair = (text, link)
                #print(pair)
                final.append(pair)
            else:
                break 


        final.reverse()

        self.wn.append('BIS - Management Speeches')
        self.websites.append(final)
        driver.quit()
        return final    

    def get_bis_workingpapers(self):
        today = self.get_month()[0:3] #Gets current month 

        url = r'https://www.bis.org/wpapers/index.htm?m=161&wppubls_page_length=15'
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-gpu") # Disables hardware acceleration through the GPU (Graphics Processing Unit). This can help avoid certain rendering issues and crashes, especially in headless mode or virtualized environments.
        options.add_argument("--no-sandbox") #  Disables Chrome's sandbox security feature. This speeds things up but reduces security isolation - generally only recommended in controlled environments like testing servers.
        options.add_argument("--disable-extensions") # Prevents Chrome extensions from loading, which saves memory and speeds up the browser's startup time.
        options.add_argument("--disable-dev-shm-usage") #Chrome uses shared memory (/dev/shm) for browser processes. This flag disables that usage, which helps prevent crashes in environments with limited memory like Docker containers.
        # set the options to use Chrome in headless mode
        options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(10)        
        driver.get(url)
        driver.find_elements(By.TAG_NAME, 'p')
        driver.find_elements(By.TAG_NAME, 'tr')

        time.sleep(3) 


        soup = BeautifulSoup(driver.page_source, 'html5lib')



        titles = soup.find_all(class_ = 'title')
        dates = soup.find_all(class_ = 'item_date')

        final = [] 
        for title,date in zip(titles, dates):

            if today.lower() in date.string.lower(): 
                link = r'https://www.bis.org' + title.a['href']
                text = title.a.span.string + title.a.span.next_sibling.string
                pair = (text, link)
                #print(pair)
                final.append(pair)
            else:
                break 

        final.reverse()

        self.wn.append('BIS - Working Papers')
        self.websites.append(final)
        driver.quit()
        return final   
    
    def get_bis_papers(self):
        today = self.get_month()[0:3] #Gets current month 

        url = r'https://www.bis.org/bispapers/index.htm?m=162&bispapers_page_length=15'
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-gpu") # Disables hardware acceleration through the GPU (Graphics Processing Unit). This can help avoid certain rendering issues and crashes, especially in headless mode or virtualized environments.
        options.add_argument("--no-sandbox") #  Disables Chrome's sandbox security feature. This speeds things up but reduces security isolation - generally only recommended in controlled environments like testing servers.
        options.add_argument("--disable-extensions") # Prevents Chrome extensions from loading, which saves memory and speeds up the browser's startup time.
        options.add_argument("--disable-dev-shm-usage") #Chrome uses shared memory (/dev/shm) for browser processes. This flag disables that usage, which helps prevent crashes in environments with limited memory like Docker containers.
        # set the options to use Chrome in headless mode
        options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(10)        
        driver.get(url)
        driver.find_elements(By.TAG_NAME, 'p')
        driver.find_elements(By.TAG_NAME, 'tr')

        time.sleep(3) 


        soup = BeautifulSoup(driver.page_source, 'html5lib')



        titles = soup.find_all(class_ = 'title')
        dates = soup.find_all(class_ = 'item_date')

        final = [] 
        for title,date in zip(titles, dates):

            if today.lower() in date.string.lower(): 
                link = r'https://www.bis.org' + title.a['href']
                text = title.a.span.string + title.a.span.next_sibling.string
                pair = (text, link)
                #print(pair)
                final.append(pair)
            else:
                break 

        final.reverse()

        self.wn.append('BIS - Papers')
        self.websites.append(final)
        driver.quit()
        return final  

    def get_bis_workingpapers(self):
        today = self.get_month()[0:3] #Gets current month 

        url = r'https://www.bis.org/wpapers/index.htm?m=161&wppubls_page_length=15'
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-gpu") # Disables hardware acceleration through the GPU (Graphics Processing Unit). This can help avoid certain rendering issues and crashes, especially in headless mode or virtualized environments.
        options.add_argument("--no-sandbox") #  Disables Chrome's sandbox security feature. This speeds things up but reduces security isolation - generally only recommended in controlled environments like testing servers.
        options.add_argument("--disable-extensions") # Prevents Chrome extensions from loading, which saves memory and speeds up the browser's startup time.
        options.add_argument("--disable-dev-shm-usage") #Chrome uses shared memory (/dev/shm) for browser processes. This flag disables that usage, which helps prevent crashes in environments with limited memory like Docker containers.
        # set the options to use Chrome in headless mode
        options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(10)        
        driver.get(url)
        driver.find_elements(By.TAG_NAME, 'p')
        driver.find_elements(By.TAG_NAME, 'tr')

        time.sleep(3) 


        soup = BeautifulSoup(driver.page_source, 'html5lib')



        titles = soup.find_all(class_ = 'title')
        dates = soup.find_all(class_ = 'item_date')

        final = [] 
        for title,date in zip(titles, dates):

            if today.lower() in date.string.lower(): 
                link = r'https://www.bis.org' + title.a['href']
                text = title.a.span.string + title.a.span.next_sibling.string
                pair = (text, link)
                #print(pair)
                final.append(pair)
            else:
                break 

        final.reverse()

        self.wn.append('BIS - Working Papers')
        self.websites.append(final)
        driver.quit()
        return final   
    
    def get_bis_ifcreports(self):
        today = self.get_month()[0:3] #Gets current month 

        url = r'https://www.bis.org/ifc_reports/index.htm'
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-gpu") # Disables hardware acceleration through the GPU (Graphics Processing Unit). This can help avoid certain rendering issues and crashes, especially in headless mode or virtualized environments.
        options.add_argument("--no-sandbox") #  Disables Chrome's sandbox security feature. This speeds things up but reduces security isolation - generally only recommended in controlled environments like testing servers.
        options.add_argument("--disable-extensions") # Prevents Chrome extensions from loading, which saves memory and speeds up the browser's startup time.
        options.add_argument("--disable-dev-shm-usage") #Chrome uses shared memory (/dev/shm) for browser processes. This flag disables that usage, which helps prevent crashes in environments with limited memory like Docker containers.
        # set the options to use Chrome in headless mode
        options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(10)        
        driver.get(url)
        driver.find_elements(By.TAG_NAME, 'p')
        driver.find_elements(By.TAG_NAME, 'tr')

        time.sleep(3) 


        soup = BeautifulSoup(driver.page_source, 'html5lib')



        titles = soup.find_all(class_ = 'title')
        dates = soup.find_all(class_ = 'item_date')

        final = [] 
        for title,date in zip(titles, dates):

            if today.lower() in date.string.lower(): 
                link = r'https://www.bis.org' + title.a['href']
                text = title.a.span.string + title.a.span.next_sibling.string
                pair = (text, link)
                #print(pair)
                final.append(pair)
            else:
                break 

        final.reverse()

        self.wn.append('BIS - IFC Reports')
        self.websites.append(final)
        
        return final  
    def get_bis_bsbreports(self):
        today = self.get_month()[0:3] #Gets current month 

        url = r'https://www.bis.org/bcbs/publications.htm?m=75'
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-gpu") # Disables hardware acceleration through the GPU (Graphics Processing Unit). This can help avoid certain rendering issues and crashes, especially in headless mode or virtualized environments.
        options.add_argument("--no-sandbox") #  Disables Chrome's sandbox security feature. This speeds things up but reduces security isolation - generally only recommended in controlled environments like testing servers.
        options.add_argument("--disable-extensions") # Prevents Chrome extensions from loading, which saves memory and speeds up the browser's startup time.
        options.add_argument("--disable-dev-shm-usage") #Chrome uses shared memory (/dev/shm) for browser processes. This flag disables that usage, which helps prevent crashes in environments with limited memory like Docker containers.
        # set the options to use Chrome in headless mode
        options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(10)        
        driver.get(url)
        driver.find_elements(By.TAG_NAME, 'p')
        driver.find_elements(By.TAG_NAME, 'tr')

        time.sleep(3) 


        soup = BeautifulSoup(driver.page_source, 'html5lib')



        titles = soup.find_all(class_ = 'title')
        dates = soup.find_all(class_ = 'item_date')

        final = [] 
        for title,date in zip(titles, dates):

            if today.lower() in date.string.lower(): 
                link = r'https://www.bis.org' + title.a['href']
                text = title.a.span.string + title.a.span.next_sibling.string
                pair = (text, link)
                #print(pair)
                final.append(pair)
            else:
                break 

        final.reverse()

        self.wn.append('BIS - BSB Reports')
        self.websites.append(final)
        driver.quit()
        return final  
    def get_bis_cpmireports(self):
        today = self.get_month()[0:3] #Gets current month 

        url = r'https://www.bis.org/cpmi_publs/index.htm?m=116'
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-gpu") # Disables hardware acceleration through the GPU (Graphics Processing Unit). This can help avoid certain rendering issues and crashes, especially in headless mode or virtualized environments.
        options.add_argument("--no-sandbox") #  Disables Chrome's sandbox security feature. This speeds things up but reduces security isolation - generally only recommended in controlled environments like testing servers.
        options.add_argument("--disable-extensions") # Prevents Chrome extensions from loading, which saves memory and speeds up the browser's startup time.
        options.add_argument("--disable-dev-shm-usage") #Chrome uses shared memory (/dev/shm) for browser processes. This flag disables that usage, which helps prevent crashes in environments with limited memory like Docker containers.
        # set the options to use Chrome in headless mode
        options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(10)        
        driver.get(url)
        driver.find_elements(By.TAG_NAME, 'p')
        driver.find_elements(By.TAG_NAME, 'tr')

        time.sleep(3) 


        soup = BeautifulSoup(driver.page_source, 'html5lib')



        titles = soup.find_all(class_ = 'title')
        dates = soup.find_all(class_ = 'item_date')

        final = [] 
        for title,date in zip(titles, dates):

            if today.lower() in date.string.lower(): 
                link = r'https://www.bis.org' + title.a['href']
                text = title.a.span.string + title.a.span.next_sibling.string
                pair = (text, link)
                #print(pair)
                final.append(pair)
            else:
                break 

        final.reverse()

        self.wn.append('BIS - CPMI Reports')
        self.websites.append(final)
        driver.quit()
        return final      

    def get_bis_cgfsreports(self):
        today = self.get_month()[0:3] #Gets current month 

        url = r'https://www.bis.org/cgfs_publs/index.htm?m=103'
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-gpu") # Disables hardware acceleration through the GPU (Graphics Processing Unit). This can help avoid certain rendering issues and crashes, especially in headless mode or virtualized environments.
        options.add_argument("--no-sandbox") #  Disables Chrome's sandbox security feature. This speeds things up but reduces security isolation - generally only recommended in controlled environments like testing servers.
        options.add_argument("--disable-extensions") # Prevents Chrome extensions from loading, which saves memory and speeds up the browser's startup time.
        options.add_argument("--disable-dev-shm-usage") #Chrome uses shared memory (/dev/shm) for browser processes. This flag disables that usage, which helps prevent crashes in environments with limited memory like Docker containers.
        # set the options to use Chrome in headless mode
        options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(10)        
        driver.get(url)
        driver.find_elements(By.TAG_NAME, 'p')
        driver.find_elements(By.TAG_NAME, 'tr')

        time.sleep(3) 


        soup = BeautifulSoup(driver.page_source, 'html5lib')



        titles = soup.find_all(class_ = 'title')
        dates = soup.find_all(class_ = 'item_date')

        final = [] 
        for title,date in zip(titles, dates):

            if today.lower() in date.string.lower(): 
                link = r'https://www.bis.org' + title.a['href']
                text = title.a.span.string + title.a.span.next_sibling.string
                pair = (text, link)
                #print(pair)
                final.append(pair)
            else:
                break 

        final.reverse()

        self.wn.append('BIS - CGFS Reports')
        self.websites.append(final)
        driver.quit()
        return final          



    def get_report_fsb(self):
        #Here we use the requests method to scrap the fsb website, since javascript is not needed to showing the content we are looking for and it is also faster.  
        today = self.get_month() #Gets name of running month 

        url = 'https://www.fsb.org/publications/'
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html5lib')

        titles = soup.find_all('div', class_ = 'post-title')

        main_container = soup.find('div', class_ = 'wp-bootstrap-blocks-row') #it gets main container
        main_container = main_container.find('div', class_ = 'display-posts-listing') #then it filters for child container where we'd like to extract dates from 
        dates = main_container.find_all('div', class_ = 'post-date')

        titles = [title.h3.a for title in titles if title.h3 is not None]
        dates = [date.span for date in dates]

        final =[]
        for title, date in zip(titles,dates): 
            if today in date.string: 
                title, link = title.string, title['href']
                final.append((title, link))
                #print(title,link)
            else:
                break 
        final.reverse()
        self.wn.append('FSB - Reports')
        self.websites.append(final)

        return final 

    def get_month_asnumber(self):
        return str(date.today())[5:7]

    def get_report_wb(self):
        today = self.get_month_asnumber()
        #print(today)
        final = []
        url = 'https://openknowledge.worldbank.org/communities/06251f8a-62c2-59fb-add5-ec0993fc20d9?spc.sf=dc.date.issued&spc.sd=DESC&spc.page=1&spc.rpp=35'

        options = webdriver.ChromeOptions()
        options.add_argument("--disable-gpu") # Disables hardware acceleration through the GPU (Graphics Processing Unit). This can help avoid certain rendering issues and crashes, especially in headless mode or virtualized environments.
        options.add_argument("--no-sandbox") #  Disables Chrome's sandbox security feature. This speeds things up but reduces security isolation - generally only recommended in controlled environments like testing servers.
        options.add_argument("--disable-extensions") # Prevents Chrome extensions from loading, which saves memory and speeds up the browser's startup time.
        options.add_argument("--disable-dev-shm-usage") #Chrome uses shared memory (/dev/shm) for browser processes. This flag disables that usage, which helps prevent crashes in environments with limited memory like Docker containers.
        # set the options to use Chrome in headless mode
        options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(25)
        stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )
        driver.get(url)

        driver.find_elements(By.CLASS_NAME, 'lead item-list-title dont-break-out ng-star-inserted notruncatable')
        driver.find_elements(By.CLASS_NAME, 'item-list-date ng-star-inserted')   
        #driver.find_element(By.CLASS_NAME, 'content dont-break-out preserve-line-breaks truncated')

        soup = BeautifulSoup(driver.page_source, 'html5lib')

        titles = soup.find_all('a', class_ = 'lead item-list-title dont-break-out ng-star-inserted notruncatable')
        dates = soup.find_all('span', class_ = 'item-list-date ng-star-inserted')
        descs = soup.find_all('div', class_ = 'content dont-break-out preserve-line-breaks truncated') #Descriptions
        report_contents = zip(titles, dates, descs)

        for title, date, desc in report_contents:
            if today in date.string[5:7] and ('report' in desc.string):
                text, link = title.string, 'https://openknowledge.worldbank.org' + title['href']
                #print(text,link)
                final.append((text,link))
  
        
        final.reverse()
        self.wn.append('World Bank - Reports')
        self.websites.append(final) 

        #driver.quit()
        return final 


    def get_wp_wb(self): #wp: working papers

        today = self.get_month_asnumber()
        #print(today)
        final = []
        url = 'https://openknowledge.worldbank.org/communities/06251f8a-62c2-59fb-add5-ec0993fc20d9?spc.sf=dc.date.issued&spc.sd=DESC&spc.page=1&spc.rpp=35'

        options = webdriver.ChromeOptions()
        options.add_argument("--disable-gpu") # Disables hardware acceleration through the GPU (Graphics Processing Unit). This can help avoid certain rendering issues and crashes, especially in headless mode or virtualized environments.
        options.add_argument("--no-sandbox") #  Disables Chrome's sandbox security feature. This speeds things up but reduces security isolation - generally only recommended in controlled environments like testing servers.
        options.add_argument("--disable-extensions") # Prevents Chrome extensions from loading, which saves memory and speeds up the browser's startup time.
        options.add_argument("--disable-dev-shm-usage") #Chrome uses shared memory (/dev/shm) for browser processes. This flag disables that usage, which helps prevent crashes in environments with limited memory like Docker containers.
        # set the options to use Chrome in headless mode
        options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(25)
        stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )
        driver.get(url)

        driver.find_elements(By.CLASS_NAME, 'lead item-list-title dont-break-out ng-star-inserted notruncatable')
        driver.find_elements(By.CLASS_NAME, 'item-list-date ng-star-inserted')   
        #driver.find_element(By.CLASS_NAME, 'list-unstyled ng-star-inserted')

        soup = BeautifulSoup(driver.page_source, 'html5lib')

        titles = soup.find_all('a', class_ = 'lead item-list-title dont-break-out ng-star-inserted notruncatable')
        dates = soup.find_all('span', class_ = 'item-list-date ng-star-inserted')
        descs = soup.find_all('div', class_ = 'content dont-break-out preserve-line-breaks truncated') #Descriptions
        
        report_contents = zip(titles, dates, descs)

        for title, date, desc in report_contents:
            if today in date.string[5:7] and 'report' not in desc.string:
                text, link = title.string, 'https://openknowledge.worldbank.org' + title['href']
                final.append((text,link))
                #print(title.string, title['href'])
        
        final.reverse()
        self.wn.append('World Bank - Working Papers')
        self.websites.append(final)           

        driver.quit()
        return final
    

    def get_wp_oecd(self): 
        today = self.get_month()[0:3]
        final = []
        options = webdriver.ChromeOptions()

        # set the options to use Chrome in headless mode
        options.add_argument("--headless=new")
        #options.add_argument("--disable-gpu") # Disables hardware acceleration through the GPU (Graphics Processing Unit). This can help avoid certain rendering issues and crashes, especially in headless mode or virtualized environments.
        #options.add_argument("--no-sandbox") #  Disables Chrome's sandbox security feature. This speeds things up but reduces security isolation - generally only recommended in controlled environments like testing servers.
        #options.add_argument("--disable-extensions") # Prevents Chrome extensions from loading, which saves memory and speeds up the browser's startup time.
        #options.add_argument("--disable-dev-shm-usage") #Chrome uses shared memory (/dev/shm) for browser processes. This flag disables that usage, which helps prevent crashes in environments with limited memory like Docker containers.


        # initialize an instance of the Chrome driver (browser) in headless mode
        driver = webdriver.Chrome(options=options)
        url = r'https://www.oecd.org/en/publications/reports.html?orderBy=mostRecent&page=0&facetTags=oecd-content-types%3Apublications%2Fworking-papers'

        #makes the scrapper more stealthy in order to bypass Cloudfare false flagging 
        stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )
        

        driver.get(url)
        driver.implicitly_wait(15)
            
        driver.find_elements(By.CLASS_NAME, 'search-result-list-item__title')
        dates_b = driver.find_elements(By.CLASS_NAME, 'search-result-list-item__date')

        pages_to_scrap = []
        #driver.execute_script("window.scrollTo(0, (document.body.scrollHeight))") #scrolls to the bottom of the page
        
        #e = driver.find_element(By.CSS_SELECTOR, '[aria-label="Next page"]')


        #for date in dates_b:
        #    print(date.text)

        a = True
        first_page = True #the process will not stop unless the first page has already been recovered. 
        #Next month's reports are published early so as to stop the script from prematurely stopping the scrapping process, this variable is created with the end of being used
        #by the condition to check whether to stop the loop early. 

        while a: 
            dates_b = driver.find_elements(By.CLASS_NAME, 'search-result-list-item__date')
            for d in dates_b:
                if today not in d.text and not first_page:
                    a = False

            if not a:
                break 
            soup = BeautifulSoup(driver.page_source, 'html5lib')
            pages_to_scrap.append(soup)        
            next_page = driver.find_element(By.CSS_SELECTOR, '[rel = "next"]')
            driver.execute_script("arguments[0].click();", next_page)
            time.sleep(2)
            first_page = False 

        for page in pages_to_scrap: 
            titles = page.find_all('div', class_ = 'search-result-list-item__title')
            dates = page.find_all('span', class_ = 'search-result-list-item__date')            
            
            for title, date in zip(titles, dates):
                if today in date.string: 
                    text, link = title.a.string, title.a['href']
                    #print(text,link)
                    final.append((text,link))



        final.reverse()
        self.wn.append('OECD - Working Papers')
        self.websites.append(final)

        return final
    
    def get_speeches_wb(self):
        today = self.get_month_asnumber()
        #today = '01' # just for testing
        final = []
        url = 'https://openknowledge.worldbank.org/communities/b6a50016-276d-56d3-bbe5-891c8d18db24?spc.sf=dc.date.issued&spc.sd=DESC'

        options = webdriver.ChromeOptions()
        options.add_argument("--disable-gpu") # Disables hardware acceleration through the GPU (Graphics Processing Unit). This can help avoid certain rendering issues and crashes, especially in headless mode or virtualized environments.
        options.add_argument("--no-sandbox") #  Disables Chrome's sandbox security feature. This speeds things up but reduces security isolation - generally only recommended in controlled environments like testing servers.
        options.add_argument("--disable-extensions") # Prevents Chrome extensions from loading, which saves memory and speeds up the browser's startup time.
        options.add_argument("--disable-dev-shm-usage") #Chrome uses shared memory (/dev/shm) for browser processes. This flag disables that usage, which helps prevent crashes in environments with limited memory like Docker containers.
        # set the options to use Chrome in headless mode
        options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(25)
        driver.get(url)

        driver.find_elements(By.CLASS_NAME, 'lead item-list-title dont-break-out ng-star-inserted notruncatable')
        driver.find_elements(By.CLASS_NAME, 'item-list-date ng-star-inserted')   
        #driver.find_element(By.CLASS_NAME, 'list-unstyled ng-star-inserted')

        soup = BeautifulSoup(driver.page_source, 'html5lib')

        titles = soup.find_all('a', 'lead item-list-title dont-break-out ng-star-inserted notruncatable')
        dates = soup.find_all('span', 'item-list-date ng-star-inserted')
        
        
        report_contents = zip(titles, dates)

        for title, date in report_contents:
            if today in date.string[5:7]:
                text, link = title.string, title['href']
                final.append((text,link))
                #print(title.string, title['href'])
        
        final.reverse()
        self.wn.append('World Bank - Speeches')
        self.websites.append(final) 

        return final 
    

    def get_imf_blogs(self):
        today = self.get_month()[0:3]
        final = []
        url = 'https://www.imf.org/en/Blogs/archive'


        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html5lib')

        #titles = soup.find_all('h2', class_ = 'card-subtitle')
        titles = soup.find_all('a', class_ = 'belt-link')

        dates = soup.find_all('div', class_ = 'card-date mb-2 text-muted')

        for title, date in zip(titles, dates): 
            if today in date.string:
                text, link = title.string, 'https://www.imf.org' + title['href']
                final.append((text,link))
        final.reverse()
        self.wn.append('IMF - Blogs')
        self.websites.append(final)

        return final 

    #Methods to retrieve websites by category
    #------------------------------------------------------
    def get_all_speeches(self):
        
        speeches = [self.get_speech_bis,
        self.get_basel_speeches,
        self.get_bisManagement_speeches,                  
        self.get_speech_fsb,
        self.get_speech_imf,
        ]#The order of the elements in the list will be printed to the website in the
        #exact same order so they should be listed in the desired order.


        for speech in speeches: 
            for t in range(0,3):
                print(f'Intento: {t + 1} de la funcion {speech}')
                try:
                    speech()
                    print('Exito')
                    break 
                except: 
                    print(f'Error en la función: {speech}')
        
        print('Speeches extraction completed succesfully.')

    def get_all_reports(self):
        
        reports = [
        self.get_report_wb,
        self.get_bis_ifcreports,
        self.get_bis_bsbreports,
        self.get_bis_cpmireports,
        self.get_bis_cgfsreports,
        self.get_report_fsb,
        self.get_fem_reports,
        self.get_imf_reports,
        self.get_oecd_reports
        ]#The order of the elements in the list will be printed to the website in the
        #exact same order so they should be listed in the desired order.


        for report in reports: 
            for t in range(0,3):
                print(f'Intento: {t + 1} de la funcion {report}')
                try:
                    report()
                    print('Exito')
                    break 
                except Exception as e: 
                    print(f'Error en la función: {report} con error {e}')
        
        print('Reports extraction completed succesfully.')

    def get_all_papers(self):

        papers = [
        self.get_bid_workingpapers,
        self.get_wp_wb,
        self.get_bis_papers,
        self.get_bis_workingpapers,
        self.get_imf_blogs,
        self.get_imf_wp,
        self.get_wp_oecd
        ] #The order of the elements in the list will be printed to the website in the
        #exact same order so they should be listed in the desired order.


        for paper in papers: 
            for t in range(0,5):
                print(f'Intento: {t + 1} de la funcion {paper}')
                try:
                    paper()
                    print('Exito')
                    break 
                except Exception as e: 
                    print(f'Error en la función: {paper}. Con error: {e}')
                    if t == 2:
                        print('Intentos agotados.')
                        return False
                    
        print('Papers extraction completed succesfully.') 


if __name__ == '__main__':
    h = Scrapper()
    h.get_wp_oecd()

