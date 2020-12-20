from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action

from .services import ScoreServices, ShopCrawler
from .serializers import LaptopSerializers
from .models import Laptop


class DataViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny, ]
    serializer_class = LaptopSerializers

    @action(methods=['GET'], detail=True)
    def get_shop_data(self, request, pk=None):
        shop_id = int(pk)
        success, failed = ShopCrawler.fetch_data(shop_id)
        data = dict(
            total=success + len(failed),
            success=success,
            failed=failed
        )
        return Response(data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def get_all_shop_data(self, request):
        total = [1, 2, 3]
        success, failed = 0, []
        for i in total:
            temp_suc, temp_failed = ShopCrawler.fetch_data(i)
            success = success + temp_suc
            failed = failed + temp_failed
        data = dict(
            total=success + len(failed),
            success=success,
            failed=failed
        )
        return Response(data, status=status.HTTP_200_OK)

    @action(methods=['DELETE'], detail=False)
    def remove_all(self, request):
        Laptop.objects.filter(id__gte=-1, train=0).delete()
        data = { 'detail': 'delete data successful' }
        return Response(data, status=status.HTTP_200_OK)

    def list(self, request):
        query_text = request.query_params.get('name', None)
        query_option = request.query_params.get('option', None)
        queryset = Laptop.objects.all().values('id', 'name', 'price')
        if query_option == 'name':
            queryset = Laptop.objects.filter(name__icontains=query_text).values('id', 'name', 'price')
        elif query_option == 'cpu':
            queryset = Laptop.objects.filter(cpu__icontains=query_text).values('id', 'name', 'price')
        return Response(queryset)

    def retrieve(self, request, pk=None):
        laptop = get_object_or_404(Laptop, pk=pk)
        serializer = self.get_serializer(laptop)
        return Response(serializer.data)

    def update(self, request, pk=None):
        laptop = Laptop.objects.filter(id=pk).first()
        if not laptop:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(laptop, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def gpu_scores(self, request):
        ScoreServices.save_gpu_scores()
        data = { 'detail': 'get gpu data done' }
        return Response(data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def cpu_scores(self, request):
        ScoreServices.save_cpu_scores()
        data = { 'detail': 'get cpu data done' }
        return Response(data, status=status.HTTP_200_OK)