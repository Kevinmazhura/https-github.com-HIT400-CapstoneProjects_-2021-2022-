
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from bs4 import BeautifulSoup
import requests
import pandas as pd
 
# Calling DataFrame constructor

class Command(BaseCommand):
    help = 'Scrap Halsteds'
    
    def get_chrome_web_driver(options):
        return webdriver.Chrome("./chromedriver", chrome_options=options)


    def get_web_driver_options():
        return webdriver.ChromeOptions()


    def set_ignore_certificate_error(options):
        options.add_argument('--ignore-certificate-errors')


    def set_browser_as_incognito(options):
        options.add_argument('--incognito')

    def handle(self, *args, **options):
        url="https://www.halsteds.co.zw/"
        source=requests.get(url)
        soup=BeautifulSoup(source.text,features="html.parser")
        product_div = soup.find_all("div", {"class": "block-products-list"})       
        my_list = []
        row = 0
        for product in product_div:
            #print(product)
            prod = product.find_all('li',{"class": "product-item"})
            for item in prod:
                print(item.a['href'])
                #print(item.a.text)
                #print(item.img['src'])
                store = "Halsteds"
                product_photo_link =item.find('a' ,{"class": "product-item-photo"})['href']
                product_price =item.find('span' ,{"class": "price"}).text
                product_detail = item.find('div' ,{"class": "product-item-details"}).a.text

                link = product_photo_link
                price = product_price.strip()
                details = product_detail.strip()

                #print(product_photo_link)
                #print( product_price.strip())
                #print( product_detail.strip())
                
                data = {"Store":store ,"Product":details,"Price":price, "Link":link}
                if len(details) >= 3:
                    my_list.append(data)
                else:
                    print('No Text')
                #print(my_list)
                #print(item)
                print("---------------------------------\n")
        df = pd.DataFrame(columns=['Store', 'Product', 'Price','Link'], data=my_list)
        print(df)

    
