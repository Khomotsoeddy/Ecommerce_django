from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
import requests
from bs4 import BeautifulSoup #For web scraping
import pandas as pd
from django.contrib import messages

from .models import Product
import random

def home(request):
    return render(request, 'store/home.html')

def sorting_product(request):
    if request.method == "POST":
        sortProduct = request.POST['sort1']
        print(sortProduct)

        if sortProduct == 'Shoprite':
            products = Product.objects.all().filter(shop_retail = 'Shoprite')
            return render(request, "store/index.html", {"products": products})
        elif sortProduct == 'Checkers':
            products = Product.objects.all().filter(shop_retail = 'Checkers')
            return render(request, "store/index.html", {"products": products})
        elif sortProduct == 'Shoprite_first':
            products = Product.objects.all().order_by('-shop_retail')
            return render(request, "store/index.html", {"products": products})
        elif sortProduct == 'Checkers_first':
            products = Product.objects.all().order_by('shop_retail')
            return render(request, "store/index.html", {"products": products})
        else:
            products = Product.objects.all()
            return render(request, "store/index.html", {"products": products})

    products = Product.objects.all()
    return render(request, "store/index.html", {"products": products})


def product_all(request):
    print(request.method)
    if request.method == "POST":
        deta =  request.POST['search_data']
        print(deta)
        if Product.objects.filter(product_name__contains=deta).exists():
            products = Product.objects.filter(product_name__contains=deta).order_by('price')
            products = products[0]
            print(products)
            return render(request, "store/index.html", {"products": products, 'isSearch': True})
        else:
            messages.info(request, "Product not found, please check your spelling")
            products = Product.objects.all()
            return render(request, "store/index.html", {"products": products})

    products = Product.objects.all()
    return render(request, "store/index.html", {"products": products})

@login_required
def get_data(request):
    user_agents_list = [
        'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
    ]
    fdfd = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.0'}
    HEADERS = {'user-agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}
    hh = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 OPR/96.0.0.0'}
    for i in range(0,10):
        print(i)
        url_shoprite = f'https://www.shoprite.co.za/c-2256/All-Departments?q=%3Arelevance%3AbrowseAllStoresFacetOff%3AbrowseAllStoresFacetOff&page={i}'
        url_checkers = f'https://www.checkers.co.za/c-2256/All-Departments?q=%3Arelevance%3AbrowseAllStoresFacetOff%3AbrowseAllStoresFacetOff&page={i+7}'
        # url_woolworths = f'https://www.woolworths.co.za/cat/Food/_/N-1z13sk5?No={i}&Ntt=groceries&Nrpp=60&inv=0'
        checkers_page = requests.get(url=url_checkers)
        shoprite_page = requests.get(url=url_shoprite)
        
        print('response type', shoprite_page)
        print('response type',checkers_page)

        shoprite_soup = BeautifulSoup(shoprite_page.content,'html.parser')
        checkers_soup = BeautifulSoup(checkers_page.content,'html.parser')

        shoprite_product = shoprite_soup.find_all('a', attrs={'class':'product-listening-click'})
        checkers_product = checkers_soup.find_all('a', attrs={'class':'product-listening-click'})
        for cp in checkers_product:
            print('product url',cp)
            product_url = 'https://www.checkers.co.za'+cp.get('href')
            print('url-->',product_url)
            checkers_product_page = requests.get(url=product_url) 

            print('----------->',checkers_product_page)

            checkers_product_soup = BeautifulSoup(checkers_product_page.content,'html.parser')
            try:
                picture_source = 'https://www.checkers.co.za'+checkers_product_soup.find('img',attrs={'class':'pdp__image__thumb'}).get('src')
                dirty_price = checkers_product_soup.find('span',attrs={'class':'now'}).text
                price = (dirty_price[2:9])
                product_name = checkers_product_soup.find('h1',attrs={'class':'pdp__name'}).text
                print("details", picture_source,'\n',price,'\n',product_name,"checkers")

                print(Product.objects.filter(shop_retail='Checkers').filter(product_name=product_name).exists())
                if Product.objects.filter(shop_retail='Checkers').filter(product_name=product_name).exists():
                    r = Product.objects.get(product_name=product_name,shop_retail='Checkers')
                    r.price = price
                    r.save()
                else:
                    r = Product(product_name=product_name,product_image=picture_source,price =price ,shop_retail='Checkers')
                    r.save()
            except Exception as e:
                print('-',e)
        for sp in shoprite_product:
            product_url = 'https://www.shoprite.co.za'+sp.get('href')
            print(product_url)
            shoprite_product_page = requests.get(url=product_url) 

            print(shoprite_product_page)

            shoprite_product_soup = BeautifulSoup(shoprite_product_page.content,'html.parser')

            try:
                picture_source = 'https://www.shoprite.co.za'+shoprite_product_soup.find('img',attrs={'class':'pdp__image__thumb'}).get('src')
                dirty_price = shoprite_product_soup.find('span',attrs={'class':'now'}).text
                price = (dirty_price[2:9])
                product_name = shoprite_product_soup.find('h1',attrs={'class':'pdp__name'}).text
                print("details", picture_source,'\n',price,'\n',product_name)

                print(Product.objects.filter(product_name=product_name).filter(shop_retail='Shoprite').exists())
                
                if Product.objects.filter(product_name=product_name).filter(shop_retail='Shoprite').exists():
                    r = Product.objects.get(product_name=product_name,shop_retail='Shoprite')
                    r.price = price
                    r.save()
                else:
                    r = Product(product_name=product_name,product_image=picture_source,price =price ,shop_retail='Shoprite')
                    r.save()
            except Exception as e:
                print('-',e)

    return render(request, "account/dashboard/dashboard.html")


def product_detail(request, id):

    product = get_object_or_404(Product.objects.all().filter(id=id))
    return render(request, "store/single.html", {"product": product})
