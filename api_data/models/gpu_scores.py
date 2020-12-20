from django.db import models


class GpuScore(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    score = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    price = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'gpu_score'

