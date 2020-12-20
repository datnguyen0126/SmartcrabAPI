import operator, re
from functools import reduce

from django.db.models import Q

from api_data.models import Laptop


class ExtractDataService:

    @classmethod
    def get_macbook(cls, pro=True, small=True, all=False):
        if all:
            if pro:
                laptops_queryset = Laptop.objects.filter(name__icontains='macbook pro')
            else:
                laptops_queryset = Laptop.objects.filter(name__icontains='macbook')
            return laptops_queryset
        keywords = []
        if pro:
            keywords.append('macbook pro')
        else:
            keywords.append('macbook air')
        if small:
            keywords.append('13.')
        else:
            keywords.append('15.')
            keywords.append('16.')
        laptops_queryset = Laptop.objects.filter(Q(reduce(operator.and_, (Q(name__icontains=x) for x in keywords))))
        return laptops_queryset

    @classmethod
    def ram_filter(cls, laptops_queryset, min=0):
        ids = [laptop.id for laptop in laptops_queryset if cls.get_ram(laptop.ram) >= min]
        return laptops_queryset.filter(id__in=ids)

    @classmethod
    def get_ram(cls, ram_text, default=0):
        ram_pattern = '\d*[GB]\w+'
        try:
            ram = re.findall(ram_pattern, ram_text)[0]
            ram_value = int(cls.replace('gb', '', ram))
            return ram_value
        except Exception:
            return default

    @classmethod
    def replace(cls, old, new, str, caseinsentive=False):
        if caseinsentive:
            return str.replace(old, new)
        else:
            return re.sub(re.escape(old), new, str, flags=re.IGNORECASE)