from bs4 import BeautifulSoup
import requests
from api_data.models import CpuScore, GpuScore
from django.db import connection


class ScoreServices:
    SQL_FILTER = '''delete FROM cpu_score where 
                    name not like 'AMD A%M%' and name not like 'AMD ryzen %U%' 
                    and name not like 'AMD ryzen %H%@%' 
                    and name not like BINARY 'Intel %M%'
                    and name not like BINARY 'Intel %U%'
                    and name not like BINARY 'Intel %H%@%'
                    and name not like BINARY 'Intel Core %G%@%';'''
    @classmethod
    def get_cpu_scores(cls):
        page_url = "https://www.cpubenchmark.net/cpu_list.php"
        response = requests.get(page_url)
        parser = BeautifulSoup(response.text, 'html.parser')
        data = []
        table = parser.find(id="cputable")
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])
        return data

    @classmethod
    def save_cpu_scores(cls):
        # clear the gpu database
        CpuScore.objects.filter(id__lt=0).delete()
        datalist = cls.get_cpu_scores()
        for data in datalist:
            try:
                temp = data[1].replace(",", "")
                temp = int(temp)
                CpuScore.objects.create(name=data[0], score=temp, rank=data[2], price=data[3])
            except ValueError:
                continue
        with connection.cursor() as cursor:
            cursor.execute(cls.SQL_FILTER)

    @classmethod
    def get_gpu_scores(cls):
        page_url = "https://www.videocardbenchmark.net/gpu_list.php"
        response = requests.get(page_url)
        parser = BeautifulSoup(response.text, 'html.parser')
        data = []
        table = parser.find(id="cputable")
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])
        return data

    @classmethod
    def save_gpu_scores(cls):
        # clear the gpu database
        GpuScore.objects.filter(id__lt=0).delete()
        datalist = cls.get_gpu_scores()
        for data in datalist:
            try:
                temp = data[1].replace(",", "")
                temp = int(temp)
                GpuScore.objects.create(name=data[0], score=temp, rank=data[2], price=data[3])
            except ValueError:
                continue
