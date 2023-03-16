from django.shortcuts import get_object_or_404, render
import requests
from bs4 import BeautifulSoup #For web scraping
import pandas as pd

from .models import Product
import random

def home(request):
    return render(request, 'store/home.html')

def product_all(request):
    # Product.objects.all().delete()

    

    user_agents_list = [
        'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
    ]
    fdfd = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.0'}
    HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}

    # for i in range(0,30):
    #     print(i)
    #     url_shoprite = f'https://www.shoprite.co.za/c-2256/All-Departments?q=%3Arelevance%3AbrowseAllStoresFacetOff%3AbrowseAllStoresFacetOff&page={i}'
    #     url_checkers = f'https://www.checkers.co.za/c-2256/All-Departments?q=%3Arelevance%3AbrowseAllStoresFacetOff%3AbrowseAllStoresFacetOff&page={i}'
    #     # url_woolworths = f'https://www.woolworths.co.za/cat/Food/_/N-1z13sk5?No={i}&Ntt=groceries&Nrpp=60&inv=0'
    #     shoprite_page = requests.get(url=url_shoprite, headers={'User-Agent': random.choice(user_agents_list)})
    #     checkers_page = requests.get(url=url_checkers,headers={'User-Agent': random.choice(user_agents_list)})

    #     print('data type', shoprite_page)
    #     print('data type',checkers_page)

    #     shoprite_soup = BeautifulSoup(shoprite_page.content,'html.parser')
    #     checkers_soup = BeautifulSoup(checkers_page.content,'html.parser')

    #     shoprite_product = shoprite_soup.find_all('a', attrs={'class':'product-listening-click'})
    #     checkers_product = checkers_soup.find_all('a', attrs={'class':'product-listening-click'})

        # for sp in shoprite_product:
        #     product_url = 'https://www.shoprite.co.za'+sp.get('href')
        #     print(product_url)
        #     shoprite_product_page = requests.get(url=product_url, headers=HEADERS) 

        #     print(shoprite_product_page)

        #     shoprite_product_soup = BeautifulSoup(shoprite_product_page.content,'html.parser')

        #     picture_source = 'https://www.shoprite.co.za'+shoprite_product_soup.find('img',attrs={'class':'pdp__image__thumb'}).get('src')
        #     dirty_price = shoprite_product_soup.find('span',attrs={'class':'now'}).text
        #     price = (dirty_price[2:11])
        #     product_name = shoprite_product_soup.find('h1',attrs={'class':'pdp__name'}).text
        #     print("details", picture_source,'\n',price,'\n',product_name)

        #     print(Product.objects.filter(product_name=product_name).filter(shop_retail='Shoprite').exists())
            
        #     if Product.objects.filter(product_name=product_name).filter(shop_retail='Shoprite').exists():
        #         r = Product.objects.get(product_name=product_name)
        #         r.price = price
        #         r.save()
        #     else:
        #         r = Product(product_name=product_name,product_image=picture_source,price =price ,shop_retail='Shoprite')
        #         r.save()

        # for cp in checkers_product:
        #     product_url = 'https://www.checkers.co.za'+cp.get('href')
        #     print(product_url)
        #     checkers_product_page = requests.get(url=product_url, headers=HEADERS) 

        #     print(checkers_product_page)

        #     checkers_product_soup = BeautifulSoup(checkers_product_page.content,'html.parser')

        #     picture_source = 'https://www.checkers.co.za'+checkers_product_soup.find('img',attrs={'class':'pdp__image__thumb'}).get('src')
        #     dirty_price = checkers_product_soup.find('span',attrs={'class':'now'}).text
        #     price = (dirty_price[2:11])
        #     product_name = checkers_product_soup.find('h1',attrs={'class':'pdp__name'}).text
        #     print("details", picture_source,'\n',price,'\n',product_name,"checkers")

        #     if Product.objects.filter(product_name=product_name).filter(shop_retail='Checkers').exists():
        #         r = Product.objects.get(product_name=product_name)
        #         r.price = price
        #         r.save()
        #     else:
        #         r = Product(product_name=product_name,product_image=picture_source,price =price ,shop_retail='Checkers')
        #         r.save()

# ==============================================================================================

    #     shoprite_data = shoprite_soup.find_all('div',attrs={'class':'item-product'})
        # checkers_data = checkers_soup.find_all('div',attrs={'class':'item-product'})

        # print(checkers_data)

    #     for pp in shoprite_data:
    #         print('pictures','https://shoprite.co.za'+pp.find('img').get('src'))
    #         print('price',pp.find('span').text)
    #         price = pp.find('span').text
    #         price1 = (price[2:])
    #         print(price1)
    #         print('title',pp.find('a').get('title'))
    #         print('\n')

    #         # r = Product.objects.get(product_name=pp.find('a').get('title'), shop_retail='Shoprite')

    #         # if r.exists:
    #         #     r.product_image = 'https://shoprite.co.za'+pp.find('img').get('src')
    #         #     r.price = price1
    #         #     r.save()
    #         # else:
    #         r = Product(product_name=pp.find('a').get('title'),product_image='https://shoprite.co.za'+pp.find('img').get('src'),price =price1 ,shop_retail='Shoprite')
    #         r.save()

    #     for pp in checkers_data:
    #         print('pictures','https://www.checkers.co.za'+pp.find('img').get('src'))
    #         print('price',pp.find('span').text)
    #         price = pp.find('span').text
    #         price1 = (price[2:])
    #         print(price1)
    #         print('title',pp.find('a').get('title'))
    #         print('\n')

    #         # r = Product.objects.get(product_name=pp.find('a').get('title'),shop_retail='Checkers')

    #         # if r.exists:
    #         #     r.product_image = 'https://www.checkers.co.za'+pp.find('img').get('src')
    #         #     r.price = price1
    #         #     r.save()
    #         # else:
    #         r = Product(product_name=pp.find('a').get('title'),product_image='https://www.checkers.co.za'+pp.find('img').get('src'),price =price1 ,shop_retail='Checkers')
    #         r.save()

    products = Product.objects.all()

    for product in products:
        print(product.product_name,'',product.price,'',product.product_image)

    return render(request, "store/index.html", {"products": products})

def product_detail(request, id):

    product = get_object_or_404(Product.objects.all().filter(id=id))
    return render(request, "store/single.html", {"product": product})
