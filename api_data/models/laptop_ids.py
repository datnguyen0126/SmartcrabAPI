from django.db import models


class LaptopId(models.Model):
    id = models.AutoField(primary_key=True)
    link = models.CharField(max_length=255, default='')
    thumbnails = models.CharField(max_length=255, default='')
    product_id = models.CharField(max_length=255, default='')

    class Meta:
        db_table = 'laptop_id'

