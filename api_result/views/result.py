from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action

from api_result.services import ClusterServices, QuestionClustering, ReplyService
from api_result.services.clusters.purpose import PurposeCluster
from api_result.services.clusters.weight import WeightCluster
from api_questions.models import Answers, Questions
from api_result.serializers import *
from api_data.models import Laptop
from api_data.serializers import LaptopSerializers


class ResultViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny, ]
    serializer_class = ClusterScoreSerializers

    @action(methods=['GET'], detail=False)
    def set_benchmark(self, request):
        ClusterServices.set_scores()
        return Response(status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=True)
    def set_benchmark_product(self, request, pk=None):
        laptop = Laptop.objects.filter(id=pk).first()
        if not laptop:
            return Response(status=status.HTTP_404_NOT_FOUND)
        ClusterServices.set_score_gpu(laptop)
        data = ClusterServices.set_score_cpu(laptop)
        serializer = self.get_serializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def cluster_data(self, request):
        queryset = ClusteringScores.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=True)
    def cluster_data_product(self, request, pk=None):
        product = ClusteringScores.objects.filter(laptop_id=pk).first()
        if not product:
            data = { 'detail': 'Product not found' }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(product)
        return Response(serializer.data)

    # set train product

    @action(methods=['POST'], detail=False)
    def set_train_products(self, request):
        laptop_ids = request.data.get('ids').split(' ')
        answer = request.data.get('content')
        check = request.data.get('check')
        if check == 'yes':
            check = 1
        else:
            check = 0
        if not answer:
            data = { 'detail': 'Please choose an answer' }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        if not laptop_ids:
            data = { 'detail': 'Laptops must not be empty' }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        QuestionClustering.set_train_products(laptop_ids, answer, check)
        return Response(status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    def get_train_products(self, request):
        answer = request.data.get('content')
        if not answer:
            data = { 'detail': 'Please choose an answer' }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        queryset = TrainData.objects.filter(answer_name__istartswith=answer)
        serializer = ClusterQuestionSerializers(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['PUT'], detail=False)
    def remove_train_product(self, request):
        laptop_id = request.data.get('laptop_id')
        answer_content = request.data.get('content')
        laptop = get_object_or_404(Laptop, pk=laptop_id)
        answer = Answers.objects.filter(content__istartswith=answer_content)
        TrainData.objects.filter(laptop=laptop, answer=answer).delete
        return Response(status=status.HTTP_204_NO_CONTENT)

    # cluster all products

    @action(methods=['POST'], detail=False)
    def check_product(self, request):
        laptop_id = request.data.get('laptop_id')
        content = request.data.get('content')
        laptop = Laptop.objects.filter(id=laptop_id).first()
        check = PurposeCluster.check_laptop(content, laptop)
        answer = Answers.objects.filter(content=content).first()
        if answer.question.id > 3:
            check = WeightCluster.check_laptop(answer, laptop)
        return Response(check, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def cluster(self, request):
        QuestionClustering.clustering()
        return Response(status=status.HTTP_200_OK)

    # get the result

    @action(methods=['POST'], detail=False)
    def get_result_products(self, request):
        answers = request.data.get('answers')
        laptops = QuestionClustering.clustering(answers)
        plids = laptops.filter(link__icontains='philong').order_by('-price').values_list('id', flat=True)[0:6]
        mgids = laptops.filter(link__icontains='mega').order_by('-price').values_list('id', flat=True)[0:4]
        xvids = laptops.filter(link__icontains='xuanvinh').order_by('-price').values_list('id', flat=True)[0:5]
        ret_ids = list(plids) + list(mgids) + list(xvids)
        laptops = laptops.filter(id__in=ret_ids).order_by('-price')
        #laptops = Laptop.objects.all()[0:5]
        if not laptops:
            data = { 'detail': 'No product found' }
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        serializer = LaptopSerializers(laptops, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
