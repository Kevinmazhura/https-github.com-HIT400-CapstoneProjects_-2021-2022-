
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
        ps = soup.find_all("ul", {"class": "brands-slider"})
        df = []
        df = pd.DataFrame(columns=['store','menu_links', 'my_items'])
        print(df)
        #print(ps)
        my_list = []
        row = 0
        for ul in ps:
            links = ul.find_all('li')
            for li in links:
                link = li.a
                text = link.text
                print("\n")
                image = li.img
                print(text ,end=" ")
                print(link['href'] ,end=" ")
                print(image['src'] ,end=" ")
                data = {"Text":text ,"Image":image['src'], "Link":link['href']}
                if len(text) >= 3:
                    my_list.append(data)
                else:
                    print('No Text')
                #print(my_list)

        df = pd.DataFrame(columns=['Text', 'Image', 'Link'], data=my_list)
        print(df)
        #menu_items = [x.text for x in links]
        #menu_links = [x.a['href'] for x in links]
        #images = [x.img['src'] for x in links]
        #store = "Halsteds"
        ##my_items = [dict(zip(menu_items,images))]
        #df.loc[row, 'store'] = store
        #df.loc[row, 'my_items'] = menu_items
        #df.loc[row, 'menu_links'] = menu_links
        #print(df.head())
        #brands-slider
        #slide = soup.findall('ul')
       
        #products-grid
    
