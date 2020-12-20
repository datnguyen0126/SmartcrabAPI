from api_data.models import Laptop
from api_data.services.crawler.data_specs import DataSpecs
from api_data.utils import FAKE_HEADER
from bs4 import BeautifulSoup
import requests, json, re

LOGO = 'https://mega.com.vn/media/banner/logo_logo web.png'
SHOP_URL = 'https://mega.com.vn'
PRODUCT_URL = 'https://mega.com.vn/hang-san-xuat.html?sort=price-asc&page={page}'


class MegaCrawler:

    @classmethod
    def get_description(cls, html_text):
        ret = ''
        try:
            for text in html_text.findAll('span'):
                ret = ret + text.text
            return ret
        except Exception:
            return ''

    @classmethod
    def get_products(cls):
        ret = []
        i = 1
        stop = False
        while True:
            source = requests.get(PRODUCT_URL.format(page=i), headers=FAKE_HEADER).text
            parser = BeautifulSoup(source, 'html.parser')
            # find list of all laptop brands
            div_all = parser.findAll('div', {"class": 'product-list'})
            div_all = div_all[1]
            if not div_all.find('div', {"class": 'p-item'}):
                stop = True
            if stop:
                break
            for div_child in div_all.findAll('div', {"class": 'p-item'}):
                temp = div_child.find('div', {"class": 'p-container'}).find('a')['href']
                if div_child.find('div', {"class": 'p-container'}).find('span', {"class": 'p-price'}).text != 'Liên hệ':
                    ret.append(temp)
                # print(div_child.find('h2').find('a')['href'])
            i = i + 1
        return ret

    @classmethod
    def get_product_info(cls, product_link):
        brand_keywords = ['Tên Hãng', 'Hãng sản xuất']
        ret = dict()
        brand = ''
        source = requests.get(SHOP_URL + product_link, headers=FAKE_HEADER).text
        parser = BeautifulSoup(source, 'html.parser')
        price = parser.find('div', {'id':'product-info-price'}).find('b', {'class':'text-20 red'}).text
        thumbnail = SHOP_URL + parser.find('div', {'id':'img-large'}).find('img')['src']
        name = parser.find('h1', {'class':'product-name'}).text
        div_description = parser.find('div', {'id':'description'})
        div_info = parser.find('div', {"class": "box-common technical-table mt-3"})
        table = div_info.find('tbody')
        for tr in table.findAll('tr'):
            tds = tr.findAll('td')
            if len(tds) < 2:
                continue
            temp = [tds[0].text.strip("\n"), tds[1].text.strip("\n")]
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
            elif temp[0] in brand_keywords:
                brand = temp[1]
            else:
                temp_dict = {
                    temp[0]: temp[1]
                }
                ret.update(temp_dict)
        return ret, str(div_description), name, price, thumbnail, brand

    @classmethod
    def fetch_data(cls):
        success = 0
        failed = []
        product_links = cls.get_products()
        for product_link in product_links:
            try:
                specs, description, name, price, thumbnail, brand = cls.get_product_info(product_link)
                clean_specs = DataSpecs.get_specifications(seller=LOGO, brand=brand,
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
