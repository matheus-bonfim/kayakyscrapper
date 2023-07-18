from selenium import webdriver
from time import sleep
import pandas as pd
from bs4 import BeautifulSoup
import os 
from selenium.webdriver.common.by import By
import random


lst_user_drivers = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36',
                    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.2 Safari/605.1.15 Chrome/94.0.4606.81'
                    ,'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
                    ]
options = webdriver.ChromeOptions()
options.add_argument('--user-agent='+lst_user_drivers[4])

driver = webdriver.Chrome(options=options)
driver.executable_path = r'./chromedriver.exe'


dia1 = 1
dia2 = 15

lst_prices = []
lst_company_names = []
lst_passages = []
lst_CheapPassages = []
d_value = 5500

def random_time():

    time_dist = [random.uniform(3,10), random.uniform(10,12)]
    probs = [0.875,0.125]
    rand_time = random.choices(time_dist, weights=probs, k=1)
    return rand_time[0]



class Passage:
        
    def __init__(self, company, price, url_oferta=0):
        url_kayak = 'https://www.kayak.com.br'
        self.company = company
        price_adj = float(price[3:])*1000
        self.price = price_adj
        self.url_oferta = url_kayak + url_oferta
        
    def show_content(self):
        lst = [self.price, self.company, self.url_oferta]
        return lst


n = 0
i=0

while dia2<=31:
    
    dia2=dia2 + 1
    if (dia2-dia1)>=21:
        dia2 = dia1 + 16
        dia1 = dia1 + 1
        
    if dia1<10:
        dia1_str = '0'+str(dia1)
    else:
        dia1_str = str(dia1)
    dia2_str = str(dia2)

    #mudando user agent
    if n >= 4:
        i+=1
        if i>4:
            i=0
        n = 0; 
        options = webdriver.ChromeOptions()
        options.add_argument('--user-agent='+lst_user_drivers[i])
        driver = webdriver.Chrome(options=options)
        driver.executable_path = r'./chromedriver.exe'
    
    

    to_location = ['LIS,OPO,FAO','BCN,GRO,REU']
    data_ida = '2024-01-{dia1}'.format(dia1=dia1_str)
    data_volta = '2024-01-{dia2}'.format(dia2=dia2_str)
    url = 'https://www.kayak.com.br/flights/CWB-{to_location}/{data1}/{data2}?sort=price_a'.format(to_location=to_location[1], data1=data_ida, data2=data_volta)
    print("data:", url)



    driver.get(url)

    # checando user agent

    user_agent = driver.execute_script("return navigator.userAgent")
    print("User agent: ",user_agent)

    if driver.current_url != url:
        sleep(30)
        driver.get(url)

    
    sleep(3)

    flight_rows = driver.find_elements(By.XPATH, '//div[@class="nrc6-wrapper"]')

    for WebElement in flight_rows:
        try:
            elementHTML = WebElement.get_attribute('outerHTML')
            elementSoup = BeautifulSoup(elementHTML, 'html.parser')

            #price
            temp_price = elementSoup.find("div", {"class":"nrc6-price-section"})
            price = temp_price.find("div", {"class":"f8F1-price-text"}) 
            company_names = elementSoup.find("div",{"class": "J0g6-operator-text"}).text   
            #url
            ver_oferta = elementSoup.find("div", {"class":"M_JD-booking-btn"})
            url_oferta = ver_oferta.find("div", {"class":"oVHK"})
            url_ofertaa = url_oferta.find("a")["href"]
            
            passage = Passage(company_names, price.text, url_ofertaa)
            if passage.price <= d_value:
                lst_CheapPassages.append(passage)
                
            lst_passages.append(passage)
        except:
            print("deu erro familia")
            continue
    
    time = random_time()
    #print("Tempooo:",time)
    sleep(time)
    #print("Passagens mais baratas:\n")
    #for pas in lst_CheapPassages:
        #print(pas.price, pas.company)
    
    n+=1

#print("passagens baratas\n")
#print(lst_CheapPassages)


lst_lowest_price = []
if len(lst_CheapPassages)>0:
    lst_lowest_price.append(lst_CheapPassages[0])

for pas in lst_CheapPassages:
    if pas.price < lst_lowest_price[0].price:
        lst_lowest_price = []
        lst_lowest_price.append(pas)
    else:
        if pas.price == lst_lowest_price[0].price:
            lst_lowest_price.append(pas)
        
if len(lst_lowest_price)>0:
    print("Passagens mais baratas:\n")
    for pas in lst_lowest_price:
        print(pas.show_content())
else:
    print("Não há nenhum voo que atenda o valor máximo de ",d_value)

