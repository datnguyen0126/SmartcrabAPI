from api_data.models import Laptop
from api_data.services.crawler.data_specs import DataSpecs
from api_data.utils import FAKE_HEADER
from bs4 import BeautifulSoup
import requests
import json, re

PREFIX_URL = 'http://xuanvinh.vn/'
LOGO = 'http://xuanvinh.vn/uploads/logo3.png'
SHOP_URL = 'http://xuanvinh.vn/may-tinh-xach-tay'
brand_url = '{brand}?page={page}'
list_brand_urls = []


class XuanVinhCrawler:

    @classmethod
    def get_laptop_brand_links(cls):
        source = requests.get(SHOP_URL, headers=FAKE_HEADER).text
        parser = BeautifulSoup(source, 'html.parser')
        # find list of all laptop brands
        div_all = parser.find('div', {"class": 'tax-child'})
        for div_child in div_all.findAll('div', {"class": 'tax-child-item'}):
            temp = div_child.find('h2').find('a')['href']
            if not any(x in temp for x in ['balo', 'linh-kien', 'Apple']):
                list_brand_urls.append(temp)

    @classmethod
    def get_product_links(cls, brand):
        ret = []
        page = None
        stop = False
        i = 1
        # product_item_in_list
        while True:
            temp_url = brand_url.format(brand=brand, page=i)
            source = requests.get(temp_url, headers=FAKE_HEADER).text
            parser = BeautifulSoup(source, 'html.parser')
            if page is None:
                page = parser.find('a', string="Trang cuối")
            list_products = parser.find('div', {"class": 'product-list'})
            for product in list_products.findAll('div', {"class": 'product-item'}):
                item_img = product.find('div', {'class': 'product-img'})
                ret.append(item_img.find('a')['href'])
            if page is None or page['href'] == temp_url:
                stop = True
            if stop:
                break
            i = i + 1
        return ret

    @classmethod
    def get_product_info(cls, product_link):
        ret = dict()
        source = requests.get(product_link, headers=FAKE_HEADER).text
        parser = BeautifulSoup(source, 'html.parser')
        name = parser.find('h1', {"class": 'single-product-title'}).text.strip()
        description = parser.find('div', {'class':'mo-ta-san-pham'})
        price = parser.find('div', {'class':'single-product-price'}).find('div').text
        thumbnail = parser.find('div', {'class':'img-main'}).find('img')['src']
        div_info = parser.find('div', {"id": "tab1"})
        table = div_info.find('tbody')
        for tr in table.findAll('tr'):
            temp = []
            for td in tr.findAll('td'):
                if td.find('p'):
                    temp.append(td.find('span').text)
                else:
                    temp.append(td.text)
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
        return ret, str(description), name, price, thumbnail

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
                    clean_specs = DataSpecs.get_specifications(seller=LOGO, brand=brand_url.split('/')[3].split('.')[0],
                                                               name=name, description=description, specs=specs,
                                                               price=price, thumbnail=thumbnail)
                    clean_specs.update(link=product_link)

                    Laptop.objects.create(**clean_specs)
                except Exception as e:
                    failed.append(product_link)
                    print(e)
                    continue
                else:
                    success = success + 1
                    print('add success')
        return success, failed

