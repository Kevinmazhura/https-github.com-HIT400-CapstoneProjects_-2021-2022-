import os
from unicodedata import category, name
from bs4 import BeautifulSoup
from django.conf import settings
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.utils.text import slugify 
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
import pandas as pd
import requests
from app.models import OnlineStore, StoreCategory , Product as OnlineProduct
from hardreco.settings import MEDIA_ROOT

from order.models import ShopCartForm
from profiles.forms import ProfileIntrestsForm
from profiles.models import Profile, ProfileIntrests
from shop.forms import StoreProductForm
from .forms import ReviewForm
from .suggestions import update_clusters
from .models import Category, Product, SubCategory, Slider, Review, Cluster


def signup(request):
    if request.method == "POST":
        # creating a user
        if request.POST['password'] == request.POST['repeatpassword']:
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'shop/Register.html', {'error': "User already exist"})
            except User.DoesNotExist:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'],
                                                email=request.POST['email'])
                created_user = User.objects.get(username=request.POST['username'])
                username= request.POST['username']
                profile = Profile.objects.create(
                    user=created_user,
                    first_name = username,
                    last_name =username,
                    email = request.POST['email'],
                    email_verify = request.POST['email'],
                    date_of_birth = datetime.date.today(),
                    bio = "",
                    avatar = "",
                    city ="",
                    district = "",
                    country_of_residence = "",
                    hobby = "",
                    slug = slugify(username),
                    )
                profile.save()
                return redirect('/')
        else:
            return render(request, 'shop/Register.html', {'error': "Password Don't match"})

    else:
        return render(request, 'shop/Register.html')


def user_login(request):
    if request.method == "POST":
        uname = request.POST['username']
        pwd = request.POST['password']
        user = auth.authenticate(username=uname, password=pwd)
        if user is not None:
            auth.login(request, user)
            return render(request, 'shop/index.html', {'error': "Invalid Login credential"})

        else:
            return render(request, 'shop/login.html', {'error': "Invalid Login credential"})
    else:
        return render(request, 'shop/login.html')


def user_logout(request):
    logout(request)
    return redirect("shop:shophome")
from django.core.exceptions import ObjectDoesNotExist

def index(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    slider = Slider.objects.all()
    electronics = SubCategory.objects.filter(Q(category_id=1))
    products = Product.objects.filter(available=True).order_by('?')[0:100]
    paginator = Paginator(products, 3)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    product_list = Product.objects.order_by('-name')
    scrapped_categories = StoreCategory.objects.all()
    online_stores = OnlineStore.objects.all()
    top_reviewed_products = Review.objects.order_by('rating')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)[:10]
    try:
        cuurent_user = User.objects.get(id=request.user.id)
        profile = Profile.objects.get(user=cuurent_user)
    except ObjectDoesNotExist:
        cuurent_user = []
        profile = []
    return render(request, 'shop/index.html', {
        'online_stores':online_stores,
        'top_reviewed_products':top_reviewed_products,
        'profile':profile,
        'scrapped_categories':scrapped_categories,
        'category': category,
        'categories': categories,
        'slider': slider,
        'electronics': electronics,
        'product_list': product_list,
        'products': paged_products})


def about(request, category_slug=None):
    category = None
    categories = Category.objects.filter(Q(name="sweate"))
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'about.html', {'category': category,
                                          'categories': categories,
                                          'products': products})


def product_list_category(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    product_list = Product.objects.order_by('-name')
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        print(category)
        products = products.filter(category=category)
    return render(request, 'shop/list.html', {'category': category,
                                              'categories': categories,
                                              'products': products,
                                              'product_list': product_list})


def search_list(request):
    print(request.GET)
    method_dir = request
    query = method_dir.GET.get('q', None)
    sugested_products = []
    if query is not None:
        lookups = Q(name__contains=query) | Q(description__contains=query)
        products = Product.objects.filter(lookups).distinct()
        for product in products:
            alt_product = Product.objects.filter(category=product.category)
            print("Alt")
            print(alt_product)
        
            sugested_products.append(alt_product)
            print("sugested_products")
            print(sugested_products)
        
        online_stores = OnlineStore.objects.all()
        catlookups = Q(name__contains=query) | Q(link__contains=query)
        
        categories = StoreCategory.objects.filter(catlookups).distinct()
        online_products = OnlineProduct.objects.filter(lookups).distinct()
        for product in online_products:
            onlineproducts = product.product_category
    else:
        products = Product.objects.none()
        online_products = OnlineProduct.objects.none()
        categories = StoreCategory.objects.none()
        

    print(products)
    print(online_products)
    print(categories)
    return render(request, 'shop/searchview.html', {'MEDIA_URL':settings.MEDIA_URL,'sugested_products':sugested_products ,'categories':categories,'products': products,'online_products':online_products})


def product_list_subcategory(request, subcategory_slug=None):
    subcategories = SubCategory.objects.all()
    products = Product.objects.filter(available=True)
    if subcategory_slug:
        subcategory = get_object_or_404(SubCategory, slug=subcategory_slug)
        print(subcategory)
        products = products.filter(subCategory=subcategory)
    return render(request, 'shop/list.html', {'subcategory': subcategory,
                                              'subcategories': subcategories,
                                              'products': products})


# def product_detail(request, id, slug):
#     product = get_object_or_404(Product, id=id, slug=slug, available=True)
#     # cart_product_form = CartAddProductForm()
#     return render(request,
#                   'shop/show.html',
#                   {'product': product})


# for recommendation

def review_list(request):
    latest_review_list = Review.objects.order_by('-pub_date')[:9]
    context = {'latest_review_list': latest_review_list}
    return render(request, 'shop/review_list.html', context)


def compare_price(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    online_products = OnlineProduct.objects.filter(name__contains=product.name)
    sugested_products = Product.objects.filter(category=product.category)
    form = ReviewForm()
    # product = []
    return render(request, 'shop/product_compare.html', {'MEDIA_URL':settings.MEDIA_URL,'products':online_products,'sugested_products':sugested_products,'product': product, 'form': form})


def open_store(request, store_id):
    store = get_object_or_404(OnlineStore, pk=store_id)
    online_products = OnlineProduct.objects.filter(store=store)
    form = ReviewForm()
    product = []
    return render(request, 'shop/store.html', {'MEDIA_URL':settings.MEDIA_URL,'products':online_products,'store': store, 'form': form})


def review_detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    return render(request, 'shop/review_detail.html', {'review': review})


def product_list(request):
    product_list = Product.objects.order_by('-name')
    context = {'product_list': product_list}
    return render(request, 'shop/product_list.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    form = ReviewForm()
    form = ShopCartForm()
    name = product.name.split()
    for nm in name:
        catlookups = Q(name__contains=product.category.name) | Q(link__contains=nm)
        online_products = OnlineProduct.objects.filter(catlookups).distinct()
    return render(request, 'shop/product_detail.html', {'MEDIA_URL':settings.MEDIA_URL,'online_products':online_products,'product': product, 'form': form})


@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        rating = form.cleaned_data['rating']
        comment = form.cleaned_data['comment']
        user_name = request.user.username
        review = Review()
        review.product = product
        review.user_name = user_name
        review.rating = rating
        review.comment = comment
        review.pub_date = datetime.datetime.now()
        review.save()
        update_clusters(is_new_user=False)

        return HttpResponseRedirect(reverse('shop:product_detail', args=(product.id,)))

    return render(request, 'shop/product_detail.html', {'product': product, 'form': form})


def user_review_list(request, username=None):
    if not username:
        username = request.user.username
    latest_review_list = Review.objects.filter(user_name=username).order_by('-pub_date')
    context = {'latest_review_list': latest_review_list, 'username': username}
    return render(request, 'shop/user_review_list.html', context)


@login_required
def user_recommendation_list(request):
    # get request user reviewed products
    profile = get_object_or_404(Profile, user=request.user)
    categories = Category.objects.all()
    my_intrests = ProfileIntrests.objects.filter(profile=profile)
    user_reviews = Review.objects.filter(user_name=request.user.username).prefetch_related('product')
    user_reviews_product_ids = set(map(lambda x: x.product.id, user_reviews))

    # get request user cluster name (just the first one right now)
    try:
        user_cluster_name = \
            User.objects.get(username=request.user.username).cluster_set.first().name
    except:  # if no cluster assigned for a user, update clusters
        update_clusters(is_new_user=True)
        user_cluster_name = \
            User.objects.get(username=request.user.username).cluster_set.first().name

    # get usernames for other memebers of the cluster
    user_cluster_other_members = \
        Cluster.objects.get(name=user_cluster_name).users \
            .exclude(username=request.user.username).all()
    other_members_usernames = set(map(lambda x: x.username, user_cluster_other_members))

    # get reviews by those users, excluding product reviewed by the request user
    other_users_reviews = \
        Review.objects.filter(user_name__in=other_members_usernames) \
            .exclude(product__id__in=user_reviews_product_ids)
    other_users_reviews_product_ids = set(map(lambda x: x.product.id, other_users_reviews))

    # then get a product list including the previous IDs, order by rating
    product_list = sorted(
        list(Product.objects.filter(id__in=other_users_reviews_product_ids)),
        key=lambda x: x.average_rating(),
        reverse=True
    )

    return render(
        request,
        'shop/user_recommendation_list.html',
        {'username': request.user.username, 'product_list': product_list}
    )
    
def Products_by_category(request):
    store_categories = StoreCategory.objects.all()
    for category in store_categories:
        df = scrap_halsteds_product_by_cat(category.link,category.name)
    halsted_object = df.to_html()
def scrap_halsteds_product_by_cat(url,cat):
    source=requests.get(url)
    print(url)
    soup= BeautifulSoup(source.text,features="html.parser")
    product_div = soup.find_all("div", {"id": "layer-product-list"})       
    my_list = []
    row = 0
    for product in product_div:
        #print(product)
        prod = product.find_all('li',{"class": "product-item"})
        for item in prod:
            # print(item.a['href'])
            #print(item.a.text)
            # print(item)
            image = item.img['data-src']
            store = "Halsteds"
            category = Category.objects.get(name=cat)
            product_photo_link =item.find('a' ,{"class": "product-item-photo"})['href']
            product_price =item.find('span' ,{"class": "price"}).text
            product_detail = item.find('div' ,{"class": "product-item-details"}).a.text
            link = product_photo_link
            price = product_price.strip()
            details = product_detail.strip()
            #print(product_photo_link)
            #print( product_price.strip())
            #print( product_detail.strip())
            subcat= SubCategory.objects.get(name="general")
            money = round(float(price[4:].replace(',','')))
            print(round(float(price[4:].replace(',',''))))
            
            data = {
                "category":category ,
                "subCategory":subcat ,
                "image_url":image,
                "name":details,
                "slug": slugify(details),
                "description":details,
                "price": money, 
                "discount_price": float(price[4:].replace(',','')), 
                "link":link,
                "stock": 10,
            }
            save_to_db(data)
            if len(details) >= 3:
                my_list.append(data)
            else:
                print('No Text')
            #print(my_list)
            #print(item)
            print("---------------------------------\n")
    df = pd.DataFrame(columns=['category', 'image', 'name','price'], data=my_list)
    print(df)
    return df
def save_to_db(data):
    # print(data['Store'])
    
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
   
    search_existing = Product.objects.filter(slug=data['slug'])
    if search_existing:
        print("product_data exist")
        print(data) 
        product =  Product.objects.get(slug=data['slug'])
        product.image_url = data['image_url']
        product.link = data['link']
        product.discount_price = data['discount_price']
        product.price = data['price']
        
        product.save()
    else:
        print("New Data")
        print(data) 
        form = StoreProductForm(data)
        if form.is_valid:
            if form.save():
                print("data saved")
            else:
                print("data not saved")
        else:
            print("Not Valid Data")
            print(data) 
    return True

