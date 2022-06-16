import mimetypes
import os
from unicodedata import category, name
from django.shortcuts import render

# Create your views here.

from django.shortcuts import HttpResponse
import pandas as pd
from bs4 import BeautifulSoup
import requests
from app.models import OnlineStore, Product, StoreCategory
from hardreco.settings import MEDIA_ROOT, MEDIA_URL
from django.utils.text import slugify 
from scrapper.forms import CategoryForm, ProductForm, StoreCategoryForm, SubCategoryForm
from shop.models import Category, SubCategory


def scrap_vaka(request):
    df = []
    # df = category_vaka()
    # df = category_ace()
    # df = save_ace_product()
    # df = save_masters()
    df = scrap_union_by_categories()
    # df = scrap_bhola()
    halsted_object = df
    return HttpResponse(halsted_object)

def scrap_bhola():
    url = "https://www.bholahardware.com/"
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }
    source=requests.get(url,headers=headers)
    soup=BeautifulSoup(source.text,features="html.parser")
    product_div = soup.find_all("li", {"id": "product"})    
    print(soup)   
    my_list = []
    row = 0
    for product in product_div:
        print(product)
    return product_div
    # https://unionhardware.co.zw/msasa/product-category/lighting-electricals/
    


def scrap_union_by_categories():
    url = "https://unionhardware.co.zw/msasa/product-category/building-materials/"
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }
    source=requests.get(url,headers=headers)
    soup=BeautifulSoup(source.text,features="html.parser")
    product_div = soup.find_all("li", {"class": "menu-item"})    
    # print(soup)   
    my_list = []
    row = 0
    for product in product_div:
        # print(product.a.text)
        # print(product.a['href'])
        category_data = {
            'name': product.a.text.strip(),
            'slug':  slugify(product.a.text.strip()),
            'online_link': product.a['href'],
            'online_image': "https://unionhardware.co.zw/msasa/wp-content/uploads/2021/02/unionlogo-1.png",
        }
        save_ace_cat(category_data)
        categ = Category.objects.get(slug=slugify(product.a.text.strip()))
        save_union_product(product.a['href'] ,categ)
        
    return product_div
    # https://unionhardware.co.zw/msasa/product-category/lighting-electricals/
    

def HalstedsCategories(request):
    df = category_halsteds()
    # df = scrap_halsteds()
    halsted_object = df.to_html()
    return HttpResponse(halsted_object)
def HalstedProducts(request):
    df = scrap_halsteds_products()
    halsted_object = df.to_html()
    return HttpResponse(halsted_object)
def HalstedProducts_by_category(request):
    store_categories = StoreCategory.objects.all()
    for category in store_categories:
        df = scrap_halsteds_product_by_cat(category.link,category.name)
    halsted_object = df.to_html()
  
    return HttpResponse(halsted_object)

def scrap_halsteds_product_by_cat(url,cat):
    source=requests.get(url)
    print(url)
    soup=BeautifulSoup(source.text,features="html.parser")
    product_div = soup.find_all("div", {"id": "layer-product-list"})       
    my_list = []
    row = 0
    for product in product_div:
        #print(product)
        prod = product.find_all('li',{"class": "product-item"})
        for item in prod:
            # print(item.a['href'])
            #print(item.a.text)
            print(item)
            image = item.img['data-src']
            store = "Halsteds"
            category = cat
            product_photo_link =item.find('a' ,{"class": "product-item-photo"})['href']
            product_price =item.find('span' ,{"class": "price"}).text
            product_detail = item.find('div' ,{"class": "product-item-details"}).a.text
            link = product_photo_link
            price = product_price.strip()
            details = product_detail.strip()
            #print(product_photo_link)
            #print( product_price.strip())
            #print( product_detail.strip())
                
            data = {"Store":store,"Category":category ,"Image":image, "Product":details,"Price":price, "Link":link}
            save_to_db(data)
            if len(details) >= 3:
                my_list.append(data)
            else:
                print('No Text')
            #print(my_list)
            #print(item)
            print("---------------------------------\n")
    df = pd.DataFrame(columns=['Store', 'Product', 'Price','Link'], data=my_list)
    print(df)
    return df

def scrap_union_categories():
    url = "https://unionhardware.co.zw/msasa/shop/"
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }
    source=requests.get(url,headers=headers)
    soup=BeautifulSoup(source.text,features="html.parser")
    product_div = soup.find_all("li", {"class","product-category"})    
    # "": ""
    my_list = []
    row = 0
    for product in product_div:
        print(product.text.split("(", 1)[0] + "_")
        print(product.a['href'])
        print(product.img['data-lazy-src'])
        # print(product.a['href'])
        category_name = product.text.split("(", 1)[0]
        category_link = product.a['href']
        category_image = product.img['data-lazy-src']
        category_data = {
            'name': category_name.strip()+"_",
            'slug':  slugify(category_name),
            'online_link': category_link,
            'online_image': category_image,
        }
        save_ace_cat(category_data)
        if category_image:
            image = category_image
            categ_data = {
                'Text': category_name,
                'Image':  image,
                'Link':  category_link,
            }
            print("categ_data")
            print(categ_data)
            save_categories(categ_data)
            # save_union_subcategory(category_link)
            categ = Category.objects.get(slug=slugify(category_name))
            # print(categ)
            save_union_subcategories(category_link,slugify(category_name),categ)
            
        else:
            print("Needs new format")
        print("\n")
        
    return product_div
def save_union_product(url,category):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }
    source=requests.get(url,headers=headers)
    soup=BeautifulSoup(source.text,features="html.parser")
    product_div = soup.find_all("li", {"class","product"})    
    # "": ""
    my_list = []
    row = 0
    for product in product_div:
        # print(product)
        store = "Union Hardware"
        details = product.h2.text
        image = product.img['src']
        link = product.a['href']
        try:
            price = product.bdi.text
            data = {
            "Store":store,
            "Category":category ,
            "Image":image,
            "Product":details,
            "Price":price, 
            "Link":link
            }
            
            print(data)
            save_to_db(data)
            if len(details) >= 3:
                my_list.append(data)
            else:
                print('No Text')
        except:
            print("price is empty")
        
        
    return product_div

def save_masters():
    url = "http://www.masters.co.zw/"
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }
    source=requests.get(url,headers=headers)
    soup=BeautifulSoup(source.text,features="html.parser")
    product_div = soup.find_all("div", {"class","panel-grid-cell"})    
    # "": ""
    my_list = []
    row = 0
    for product in product_div:
        product_li = product.find("div", {"class","textwidget"}) 
        # product_img = product.find("img", {"class","ls-bg"}) 
        try:
            image = product_li.img
            print("product_li \n") 
            print(image['title']) 
            if image:  
                img_src = image['src']
                category_link = product_li.a['href']
                category_name = image['title']
                print("src :" + img_src + "link :" + category_link)
                category_data = {
                    'name': category_name,
                    'slug':  slugify(category_name),
                    'online_link': category_link,
                    'online_image': img_src,
                }
                save_ace_cat(category_data)
                categ_data = {
                    # 'image':  path,
                    'Text': category_name,
                    'Image':   img_src,
                    'Link':  category_link,
                }
                save_categories(categ_data)
                scrap_masters_products(category_link,category_name)
                
        except:
            print("No Image Data")

        
    return product_div
def scrap_masters_products(url ,category):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }
    source=requests.get(url,headers=headers)
    soup=BeautifulSoup(source.text,features="html.parser")
    product_div = soup.find_all("li", {"class","product"})    
    # "": ""
    my_list = []
    row = 0
    for product in product_div:
        print(product)
        store = "Masters"
        image = product.img['src']
        details = product.h2.text
        price = "0"
        link = product.a['href']
        data = {
            "Store":store,
            "Category":category ,
            "Image":image,
            "Product":details,
            "Price":price, 
            "Link":link
            }
        
        print(data)
        save_to_db(data)
        if len(details) >= 3:
            my_list.append(data)
        else:
            print('No Text')
        
    return product_div
    
def category_vaka():
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }

    url="http://vaka.co.zw//"
    source=requests.get(url,headers=headers)
    soup=BeautifulSoup(source.text,features="html.parser")
    product_div = soup.find_all("div", {"class","ftr-product"})    
    # "": ""
    # print(product_div)   
    my_list = []
    row = 0
    for product in product_div:
        #print(product)
        prod = product.find_all('div',{"class": "sk-product"})
        for item in prod:
            # print(item)
            image = item.img
            src = image['src']
            link = item.a['href']
            store = "Vaka"
            cat = "Building"
            # product_photo_link =item.find('div' ,{"class": "rt-img"})
            product_price =item.find('ul' ,{"class": "price"}).text
            product_detail = item.find('a' ,{"class": "sk-heading"}).text
            print(link)
            # link = product_photo_link
            price = product_price.strip()
            details = product_detail.strip()
            data = {
                "Store":store,
                "Category":cat ,
                "Image":src,
                "Product":details,
                "Price":price, 
                "Link":link
                }
            
            print(data)
            save_to_db(data)
            if len(details) >= 3:
                my_list.append(data)
            else:
                print('No Text')
    return product_div
    
def category_ace():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }
    url="https://www.acehardware.com/departments"
    source=requests.get(url,headers=headers)
    soup=BeautifulSoup(source.text,features="html.parser")
    product_div = soup.find_all("ul", {"class","mz-facetingform-hierarchy-wrap"})    
    # "": ""
    print(product_div)   
    my_list = []
    row = 0
    for product in product_div:
        #print(product)
        prod = product.find_all('a',{"class": "mz-facetingform-link"})
        for li in prod:
            category_name = li.text
            category_link = li['href']
            # print(category_name + ":" + category_link)
            category_data = {
                'name': category_name,
                'slug':  slugify(category_name),
                'online_link': category_link,
                'online_image':  "//cdn-tp3.mozu.com/24645-37138/cms/37138/files/store-location-logo.svg",
            }
            save_ace_cat(category_data)
            categ = Category.objects.get(slug=slugify(category_name))
            # print(categ)
            link = "https://unionhardware.co.zw/msasa/shop/"+ slugify(category_name)[:-1]
            save_subcategories(link,slugify(category_name),categ)
            # save_ace_product(url,slugify(category_name))
    return product_div

def save_ace_product():
    category_ = SubCategory.objects.all()
    for category in category_:
        headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
        }
        url="https://www.acehardware.com/departments/"+category.category.name + "/" + category.slug
        # print(url)
        source=requests.get(url,headers=headers)
        soup=BeautifulSoup(source.text,features="html.parser")
        product_li = soup.find_all("li", {"mz-productlist-item"})  
         
        
           
        # "": ""
        # print(product_div)   
        my_list = []
        row = 0
        for li in product_li:
            product_div = li.find_all("div", {"class","mz-productlisting-info"}) 
            for product in product_div:
                # print(product)   
                
                product_price =product.find('div' ,{"class": "mz-pricestack"})
                price =product_price.find('span' ,{"class": "custom-price"})
                image =li.find("img", {"class","prim-img"}) 
                
                print(image['data-src'])
                try:
                    if len(price.text) >= 3:
                        print(price.text)
                        
                        store = "Ace Hardware"
                        details =  product.a.text
                        link = product.a['href']
                        image = image['data-src']
                        cat = SubCategory.objects.get(slug=category.slug)
                        data = {
                            "Store":store,
                            "Category":cat.category ,
                            "Image":image,
                            "Product":details,
                            "Price":price.text, 
                            "Link":link
                            }
                        
                        print(data)
                        save_to_db(data)
                        if len(details) >= 3:
                            my_list.append(data)
                        else:
                            print('No Text')
                except:
                    print('Invalid Price Text')
        
    return product_div
def save_subcategories(url,category_name,categ):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }

    url=url+"/"+category_name
    # print("scarp url : " + url)
    source=requests.get(url,headers=headers)
    soup=BeautifulSoup(source.text,features="html.parser")
    product_li = soup.find_all("a", {"class","picture-link"})    
    print(product_li)  
    my_list = []
    row = 0
    for li in product_li:
        subcategory_name = li.span.text
        subcategory_link = li['href']
        image = li.img['data-src']
        print("Sub Category : " + subcategory_name + ":" + subcategory_link)
        category_data = {
            'name': subcategory_name,
            'slug':  slugify(subcategory_name),
            'category': categ,
        }
        save_ace_subcat(category_data)
        if image:
            image = image
            categ_data = {
                # 'image':  path,
                'Text': subcategory_name,
                'Image':  image,
                'Link':  subcategory_link,
            }
            print("categ_data")
            print(categ_data)
            save_categories(categ_data)
            
        else:
            print("Needs new format")
        
        
    
                    
    return product_li

def save_union_subcategories(url,category_name,categ):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }

    url=url.strip()
    print("scrap url :" + url)
    source=requests.get(url,headers=headers)
    soup=BeautifulSoup(source.text,features="html.parser")
    print(soup)
    product_div = soup.find_all("div", {"class","col-cat"})    
    print(product_div)  
    my_list = []
    row = 0
    for div in product_div:
        links = div.find_all("li")  
        for product_li in links:
            subcategory_name = product_li.a.text
            subcategory_link = product_li.a['href']
            image = product_li.img['data-lazy-src']
            print("Sub Category : " + subcategory_name + ":" + subcategory_link)
            category_data = {
                'name': subcategory_name,
                'slug':  slugify(subcategory_name),
                'category': categ,
            }
            save_ace_subcat(category_data)
            if image:
                image = image
                categ_data = {
                    # 'image':  path,
                    'Text': subcategory_name,
                    'Image':  image,
                    'Link':  subcategory_link,
                }
                print("categ_data")
                print(categ_data)
                save_categories(categ_data)
                
            else:
                print("Needs new format")
        
        
    
                    
    return product_div
def scrap_halsteds_products():
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }
    url="https://www.halsteds.co.zw/"
    source=requests.get(url,headers=headers)
    soup=BeautifulSoup(source.text,features="html.parser")
    product_div = soup.find_all("div", {"class": "block-products-list"})       
    my_list = []
    row = 0
    for product in product_div:
        #print(product)
        prod = product.find_all('li',{"class": "product-item"})
        for item in prod:
            # print(item.a['href'])
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
            save_to_db(data)
            if len(details) >= 3:
                my_list.append(data)
            else:
                print('No Text')
            #print(my_list)
            #print(item)
            print("---------------------------------\n")
    df = pd.DataFrame(columns=['Store', 'Product', 'Price','Link'], data=my_list)
    print(df)
    return df

def scrap_halsteds():
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
            save_categories(data)
            if len(text) >= 3:
                my_list.append(data)
            else:
                print('No Text')
            #print(my_list)

        df = pd.DataFrame(columns=['Text', 'Image', 'Link'], data=my_list)
        print(df)
        return df
  
def save_categories(data):
    category_data = {
        # 'image':  path,
        'name': data['Text'],
        'image':   data['Image'],
        'link':  data['Link'],
    }
    search_existing = StoreCategory.objects.filter(name=data['Text'])
    if search_existing:
        print("category_data exist")
        print(category_data) 
    else:
        print("New Data")
        # print(category_data) 
        form = StoreCategoryForm(category_data)
        if form.is_valid:
            if form.save():
                print("data saved")
                
            else:
                print("data not saved")
        else:
            print("Not Valid Data")
            print(category_data) 
    return True
def category_halsteds():
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
            # print("\n")
            image = li.img
            # print(text ,end=" ")
            # print(link['href'] ,end=" ")
            print(image['src'] ,end=" ")
            data = {"Text":text ,"Image":image['src'], "Link":link['href']}
            # print(data)
            save_categories(data)
            if len(text) >= 3:
                my_list.append(data)
                save_cat(data)
            else:
                print('No Text')
            #print(my_list)

        df = pd.DataFrame(columns=['Text', 'Image', 'Link'], data=my_list)
        print(df)
        return df
def save_cat(data):
    category_data = {
        'name': data['Text'],
        'slug':  slugify(data['Text']) ,
        'online_link':  data['Link'],
        'online_image':  data['Image'],
    }
    search_existing = Category.objects.filter(slug=slugify(data['Text']))
    if search_existing:
        print("category_data exist")
        print(category_data) 
    else:
        print("New Data")
        print(category_data) 
        form = CategoryForm(category_data)
        if form.is_valid:
            if form.save():
                print("data saved")
            else:
                print("data not saved")
        else:
            print("Not Valid Data")
            print(category_data) 
    return True
def save_ace_cat(data):
    search_existing = Category.objects.filter(slug=data['slug'])
    if search_existing:
        print("category_data exist")
        print(data) 
    else:
        print("New Data")
        print(data) 
        form = CategoryForm(data)
        if form.is_valid:
            if form.save():
                print("data saved")
            else:
                print("data not saved")
        else:
            print("Not Valid Data")
            print(data) 
    return True
def save_ace_subcat(data):
    search_existing = SubCategory.objects.filter(slug=data['slug'])
    if search_existing:
        print("category_data exist")
        print(data) 
    else:
        print("New Data")
        print(data) 
        form = SubCategoryForm(data)
        if form.is_valid:
            if form.save():
                print("data saved")
            else:
                print("data not saved")
        else:
            print("Not Valid Data")
            print(data) 
    return True

def save_to_db(data):
    print(data['Store'])
    store = OnlineStore.objects.get(name=data['Store'])
    category = Category.objects.get(name=data['Category'])
    # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Define text file name
    filename = 'frame.png'
    # Define the full file path
    # filepath = MEDIA_ROOT + filename
    # Open the file for reading content
    # path = open(filepath, 'r')
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Define text file name
   
    # Define the full file path
    filepath = MEDIA_ROOT + filename
    # Open the file for reading content
    path = open(filepath, 'r')
    # Return the response value
    product_data = {
        # 'image':  path,
        'name': data['Product'],
        'store':  store,
        'product_category':  category,
        'online_image_url':data['Image'],
        'description':  data['Product'],
        'price':  data['Price'],
        'link':  data['Link'],
    }
    search_existing = Product.objects.filter(name=data['Product'][:10])
    if search_existing:
        print("product_data exist")
        print(product_data) 
        product =  Product.objects.get(name=data['Product'][:10])
        product.online_image_url = data['Image']
        product.product_category = category
        product.save()
    else:
        print("New Data")
        print(product_data) 
        form = ProductForm(product_data)
        if form.is_valid:
            if form.save():
                print("data saved")
            else:
                print("data not saved")
        else:
            print("Not Valid Data")
            print(product_data) 
    return True