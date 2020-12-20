from api_questions.models import Answers, Questions
from api_result.models import ClusteringScores, TrainData
from .clusters import *
from api_data.models import Laptop
import operator
from django.db.models import Q
from functools import reduce


class QuestionClustering:

    @classmethod
    def set_train_products(cls, ids, answer, check):
        answer = Answers.objects.filter(content=answer).first()
        for id in ids:
            item = Laptop.objects.filter(id=id).first()
            item.train = 1
            item.save()
            TrainData.objects.create(laptop_name=item.name, laptop=item, answer_name=answer.content, answer=answer,
                                     check=check)

    @classmethod
    def clustering(cls, answers):
        queryset = None

        # money
        money_answer = answers[0]
        if money_answer:
            if money_answer == 'Unlimited':
                queryset = Laptop.objects.filter(price__gte=0)
            else:
                try:
                    price = int(money_answer.split(' ')[2])
                    queryset = Laptop.objects.filter(price__lte=price)
                except ValueError:
                    print('Not value price')

        # screen size
        if len(answers) > 4 and answers[4]:
            screen_size_answer = ScreenSizeCluster.get_value(answers[4])
            if screen_size_answer:
                queryset = queryset.filter(reduce(operator.or_, (Q(screen_size__icontains=x) for x in screen_size_answer)))

        # cpu
        if len(answers) > 6:
            cpu_answer = answers[6]
            if cpu_answer and len(cpu_answer) > 0:
                queryset = queryset.filter(reduce(operator.or_, (Q(cpu__icontains=x) for x in cpu_answer)))

        # vga
        if len(answers) > 7:
            gpu_answer = answers[7]
            if gpu_answer and len(gpu_answer) > 0:
                queryset = queryset.filter(reduce(operator.or_, (Q(vga__icontains=x) for x in gpu_answer)))

        # brand
        if len(answers) > 2:
            brand_answer = answers[2]
            if 'Any' not in brand_answer:
                if brand_answer and len(brand_answer) > 0:
                    queryset = queryset.filter(reduce(operator.or_, (Q(brand__icontains=x.lower()) for x in brand_answer)))

        # os
        if len(answers) > 5:
            os_answer = answers[5]
            if os_answer:
                if os_answer == "Microsoft windows":
                    queryset = queryset.exclude(Q(name__icontains='macbook') | Q(name__icontains='apple'))
                elif os_answer == "Mac os":
                    queryset = queryset.filter(Q(name__icontains='macbook') | Q(name__icontains='apple'))
                elif os_answer == "Linux":
                    queryset = queryset.filter(reduce(operator.or_, (Q(name__icontains=x) for x in ['dell', 'thinkpad', 'thinkbook'])))

        # features
        if len(answers) > 3:
            feature_answer = answers[3]
            if feature_answer:
                queryset = FeatureCluster.feature_cluster(feature_answer)

        # purpose
        if len(answers) > 1:
            purpose_answer = answers[1]
            queryset = PurposeCluster.cluster_purpose(queryset, purpose_answer)

        # weight
        if len(answers) > 8:
            weight_answer = answers[8]
            if weight_answer:
                queryset = WeightCluster.weight_cluster(weight_answer)
        return queryset
