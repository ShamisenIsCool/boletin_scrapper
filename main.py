from bs4 import BeautifulSoup #imports library for web scrapping  
from scrapper import Scrapper
from datetime import datetime

def main(): 

    scrapped_data = [] #Storage for links that are scrapped
    
    links_actualizados =[r'https://www.imf.org/en/Publications/Search#sort=%40imfdate%20descending&numberOfResults=20&f:series=[WRKNGPPRS]', 
                     ]
    


    month = datetime.now().strftime('%B') #Da igual a el nombre del mes en curso, en ingles    
    scrapper = Scrapper(links_list=links_actualizados, month = month ) #Inicializa Objeto

    with open('links.csv', 'w') as file: 
        pass 

    print(scrapper.get_imf_wp())



main()
