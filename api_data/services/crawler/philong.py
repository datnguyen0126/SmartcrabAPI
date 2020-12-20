from api_data.utils import FAKE_HEADER
from bs4 import BeautifulSoup
import requests
from .data_specs import DataSpecs
import json, re

from ...models import Laptop

LOGO = 'http://philong.com.vn/media/banner/logo_logo_logo.philong.png'
SHOP_URL = 'https://philong.com.vn'
brand_url = SHOP_URL + '{brand}?page={page}'
list_brand_urls = []


class PhiLongCrawler:

    @classmethod
    def get_description(cls, html_text):
        if not html_text:
            return ''
        ret = ''
        try:
            for text in html_text.findAll('span'):
                ret = ret + text.text
            return ret
        except Exception:
            return ''

    @classmethod
    def get_laptop_brand_links(cls):
        source = requests.get(SHOP_URL, headers=FAKE_HEADER).text
        parser = BeautifulSoup(source, 'html.parser')
        # find list of all laptop brands
        ul = parser.find('ul', {"class": 'ul child3'})
        for li in ul.findAll('li',recursive=False):
            list_brand_urls.append(li.find('a')['href'])

    @classmethod
    def get_product_links(cls, brand):
        ret = []
        stop = False
        i = 1
        # product_item_in_list
        while True:
            source = requests.get(brand_url.format(brand=brand, page=i), headers=FAKE_HEADER).text
            parser = BeautifulSoup(source, 'html.parser')
            list_products = parser.find(id='product_item_in_list')
            if list_products and list_products.find('a', {"class": 'p-img'}):
                for product in list_products.findAll('a', {"class": 'p-img'}):
                    ret.append(product['href'])
                i = i + 1
            else:
                break
        return ret

    @classmethod
    def get_product_info(cls, product_link):
        ret = dict()
        source = requests.get(SHOP_URL + product_link, headers=FAKE_HEADER).text
        parser = BeautifulSoup(source, 'html.parser')
        name = parser.find('div', {'class': 'entry-header'}).find('h1').text
        price = parser.find('span', {'class':"p-price"}).text
        thumbnail = SHOP_URL + parser.find('a', {'id':'Zoomer'}).find('img')['src']
        div_description = parser.find('div', {"class": "entry-content productDescription"})
        div_info = parser.find('div', {"class": "tbl-technical"})
        try:
            table = div_info.find('table')
            for tr in table.findAll('tr'):
                temp = []
                if tr.find('th'):
                    temp.append(tr.find('th').text)
                    if tr.find('p'):
                        temp.append(tr.find('p').text)
                    else:
                        temp.append(tr.find('td').text)
                else:
                    for td in tr.findAll('td'):
                        if td.find('p'):
                            temp.append(td.find('p').text)
                        else:
                            temp.append(td.text)
                if len(temp) < 2:
                    continue
                if temp[0] == 'Dung lượng':
                    if 'ddr' in temp[1].lower():
                        temp_dict = {
                            'ram': temp[1]
                        }
                        ret.update(temp_dict)
                    else:
                        temp_dict = {
                            'disk': temp[1]
                        }
                        ret.update(temp_dict)
                else:
                    if len(temp) > 1:
                        temp_dict = {
                            temp[0].strip(): temp[1]
                        }
                        ret.update(temp_dict)
        except Exception:
            pass
        return ret, cls.get_description(div_description), name, price, thumbnail

    @classmethod
    def fetch_data(cls):
        cls.get_laptop_brand_links()
        success = 0
        failed = []
        for brand_url in list_brand_urls:
            product_links = cls.get_product_links(brand_url)
            for product_link in product_links:
                try:
                    specs, description, name, price, thumbnail = cls.get_product_info(product_link)
                    clean_specs = DataSpecs.get_specifications(seller=LOGO, brand=brand_url.split('-')[1].split('.')[0],
                                                                   name=name, description=description, specs=specs,
                                                                   price=price, thumbnail=thumbnail)
                    clean_specs.update(link=SHOP_URL + product_link)
                    Laptop.objects.create(**clean_specs)
                except Exception as e:
                    failed.append(SHOP_URL + product_link)
                    print(e)
                    continue
                else:
                    success = success + 1
                    print('add success')
        # for macbook
        product_links = cls.get_product_links('/macbook.html')
        for product_link in product_links:
            try:
                specs, description, name, price, thumbnail = cls.get_product_info(product_link)
                clean_specs = DataSpecs.get_specifications(seller=LOGO, brand='Apple',
                                                           name=name, description=description, specs=specs,
                                                           price=price, thumbnail=thumbnail)
                clean_specs.update(link=SHOP_URL + product_link)
                Laptop.objects.create(**clean_specs)
            except Exception as e:
                failed.append(SHOP_URL + product_link)
                print(e)
                continue
            else:
                success = success + 1
                print('add success')
        return success, failed
