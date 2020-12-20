import re

from api.utils import Utils
from api_result.models import ClusteringScores, TrainData


class WeightCluster:
    k = 9

    option = ["Very light", "Medium", "Don't bother"]

    @classmethod
    def weight_cluster(cls, laptop_queryset, answer):
        if answer == cls.option[2]:
            return laptop_queryset
        ids = [laptop.id for laptop in laptop_queryset if cls.check_laptop(answer, laptop)]
        temp_laptops = laptop_queryset(id__in=ids)
        return temp_laptops

    @classmethod
    def extract_values(cls, text, key): # cm for dimension and kg for weight
        pattern = '\d*\.?\d+'
        values = re.findall(pattern, text)
        ret = []
        if key == 'dimension':
            for value in values:
                value = Utils.convert_to_float(value)
                if 'mm' in text:
                    value = value / 1000
                ret.append(value)
        if key == 'weight':
            for value in values:
                value = Utils.convert_to_float(value)
                if value > 50 and 'kg' not in text and 'g' in text:
                    value = value / 1000
                ret.append(value)
        return ret

    @classmethod
    def get_value(cls, screen_size):
        pattern = '\d*\.?\d+'
        return re.findall(pattern, screen_size)[0]

    @classmethod
    def distance(cls, check_laptop, train_laptop):
        laptop1_dimensions = cls.extract_values(check_laptop.dimension, 'dimension')
        laptop2_dimensions = cls.extract_values(train_laptop.dimension, 'dimension')
        laptop1_weight = cls.extract_values(check_laptop.weight, 'weight')
        laptop2_weight = cls.extract_values(train_laptop.weight, 'weight')
        laptop1_screen_size = cls.get_value(check_laptop.screen_size)
        laptop2_screen_size = cls.get_value(train_laptop.screen_size)

        x1 = laptop1_dimensions[0]
        x2 = laptop2_dimensions[0]
        y1 = laptop1_dimensions[1]
        y2 = laptop2_dimensions[1]
        z1 = laptop1_dimensions[2]
        z2 = laptop2_dimensions[2]
        w1 = laptop1_weight[0]
        w2 = laptop2_weight[0]
        s1 = laptop1_screen_size
        s2 = laptop2_screen_size

        return (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2) + (z1 - z2) * (z1 - z2) + (w1 - w2) * (w1 - w2) + (s1 - s2) * (s1 - s2)

    @classmethod
    def check_laptop(cls, purpose, laptop):
        train_data = TrainData.objects.filter(answer_name__icontains=purpose)
        nearest = [None] * cls.k
        for item in train_data:
            if item == laptop:
                return True
            temp = dict(check=item.check, distance=cls.distance(laptop, item))
            if temp['distance'] == -1:
                return True
            for i in range(len(nearest)):
                if nearest[i] is None:
                    break
                else:
                    if nearest[i]['distance'] > temp['distance']:
                        if i != len(nearest) - 1:
                            nearest[i + 1] = nearest[i]
            nearest[i] = temp
        yes = 0
        for i in nearest:
            if i['check']:
                yes = yes + 1
        if yes > cls.k / 2:
            return True
        return False