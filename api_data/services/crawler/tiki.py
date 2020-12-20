from api_data.utils import FAKE_HEADER
from bs4 import BeautifulSoup
import json, re, requests
from django.db import IntegrityError

from api_data.models import Laptop, LaptopId, LaptopBackup
from api_data.utils import *

LOGO = 'https://salt.tikicdn.com/ts/upload/35/1f/42/881848473f9a789fc562d1a9cdac8ca2.png'
LAPTOPS_URL = "https://tiki.vn/laptop/c8095?src=c.8095.hamburger_menu_fly_out_banner&page={page}"
SHOP_URL = 'https://tiki.vn'
API_GET_ITEM = "https://tiki.vn/api/v2/products/{id}"


class TikiCrawler:

    @classmethod
    def get_product_id(cls):
        product_list = []
        i = 1
        while True:
            print("Crawl page: ", i)
            source = requests.get(LAPTOPS_URL.format(page=i), headers=FAKE_HEADER).text
            parser = BeautifulSoup(source, 'lxml')
            product_ids_list = parser.findAll(class_="product-item")
            if len(product_ids_list) == 0:
                break
            for product in product_ids_list:
                product_list.append(product.get("data-id"))
            i += 1
        return product_list

    @classmethod
    def get_product(cls, item_id):
        result = {}
        url = API_GET_ITEM.format(id=item_id)
        response = requests.get(url, headers=FAKE_HEADER)
        try:
            if response.status_code == 200:
                data = json.loads(response.text)
                for field in ITEM_FIELDS:
                    if field != ITEM_FIELDS[-1]:
                        result[field] = data.get(field)
                    else:
                        specs_data = data.get(ITEM_FIELDS[-1])
                        if specs_data:
                            specs_data = get_specifications(specs_data)
                            result = { **result, **specs_data }
            return result
        except Exception:
            return

    @classmethod
    def fetch_data(cls):
        success = 0
        failed = []
        item_ids = cls.get_product_id()
        for item_id in item_ids:
            data = cls.get_product(item_id)
            try:
                LaptopBackup.objects.create(**data)
            except IntegrityError:
                continue
            else:
                success = success + 1
                print('add success')
        return success, failed

    @classmethod
    def clean_data(cls):
        queryset = LaptopBackup.objects.all()
        for item in queryset:
            res = clean_data(item)
            if not item.cpu:
                item.cpu = res.get('cpu')
            if not item.ram:
                item.ram = res.get('ram')
            if not item.vga:
                item.vga = res.get('vga')
            if not item.disk:
                item.disk = res.get('disk')
            if not item.display:
                item.display = res.get('display')
            if not item.screen_size:
                item.screen_size = res.get('screen_size')
            if not item.battery:
                item.battery = res.get('battery')
            item.save()

    @classmethod
    def backup_data(cls):
        queryset = Laptop.objects.all()
        for item in queryset:
            if not (item.cpu and item.dimension and item.weight and item.ram):
                temp_laptop = LaptopBackup()
                temp_laptop.__dict__ = item.__dict__.copy()
                temp_laptop.save()

    @classmethod
    def restore_data(cls):
        items = LaptopBackup.objects.all()
        for item in items:
            temp_laptop = Laptop()
            temp_laptop.__dict__ = item.__dict__.copy()
            temp_laptop.save()
