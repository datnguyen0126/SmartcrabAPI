from functools import reduce

from django.db.models import Q

from api_data.models import Laptop
import operator

_list_answer = ["Touchscreen laptop", "Having SSD", "Working in low light conditions", "Fingerprint"]

class FeatureCluster:

    # "Touchscreen laptop",
    # "Working with a lot of numbers",
    # "Working in low light conditions",
    # "Fingerprint",

    @classmethod
    def feature_cluster(cls, laptop_queryset, answer):
        if _list_answer[0] in answer:
            laptop_queryset = cls.get_touchscreen(laptop_queryset)
        if _list_answer[1] in answer:
            laptop_queryset = cls.get_ssd(laptop_queryset)
        if _list_answer[2] in answer:
            laptop_queryset = cls.get_backlit_keyboard(laptop_queryset)
        if _list_answer[3] in answer:
            laptop_queryset = cls.get_fingerprint(laptop_queryset)
        return laptop_queryset

    @classmethod
    def get_fingerprint(cls, laptop_queryset):
        keywords = ['vân tay', 'fingerprint']
        return laptop_queryset.filter(reduce(operator.or_, (Q(description__icontains=x) for x in keywords)))

    @classmethod
    def get_touchscreen(cls, laptop_queryset):
        keywords = ['cảm ứng', ' 360 ', ' touch screen']
        return laptop_queryset.filter(reduce(operator.or_, (Q(description__icontains=x) for x in keywords)))

    @classmethod
    def get_backlit_keyboard(cls, laptop_queryset):
        keywords = ['đèn nền', 'đèn bàn phím', 'backlit']
        return laptop_queryset.filter(reduce(operator.or_, (Q(description__icontains=x) for x in keywords)))

    @classmethod
    def get_ssd(cls, laptop_queryset):
        return laptop_queryset.filter(disk__icontains='ssd')