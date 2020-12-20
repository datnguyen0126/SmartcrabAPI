from django.db import models

from api_data.models import Laptop, CpuScore, GpuScore


class ClusteringScores(models.Model):
    laptop_cpu = models.CharField(max_length=255, null=True, blank=True)
    laptop_gpu = models.CharField(max_length=255, null=True, blank=True)
    detected_cpu = models.CharField(max_length=255, null=True, blank=True)
    detected_cpu_score = models.CharField(max_length=255, null=True, blank=True)
    detected_gpu = models.CharField(max_length=255, null=True, blank=True)
    detected_gpu_score = models.CharField(max_length=255, null=True, blank=True)
    # related files if needed
    laptop = models.ForeignKey(Laptop, related_name='laptop', on_delete=models.CASCADE)
    cpu_score = models.ForeignKey(CpuScore, on_delete=models.CASCADE, related_name='cpu', null=True, blank=True)
    gpu_score = models.ForeignKey(GpuScore, on_delete=models.CASCADE, related_name='gpu', null=True, blank=True)

    class Meta:
        db_table = 'laptop_score'

