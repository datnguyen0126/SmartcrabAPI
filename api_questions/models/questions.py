from django.db import models


class Questions(models.Model):
    id = models.IntegerField(primary_key=True)
    content = models.CharField(max_length=255, blank=True, null=True)
    required = models.BooleanField(default=True)
    multiple = models.BooleanField(default=True)
    spec = models.BooleanField(default=True)
    train = models.BooleanField(default=False)

    class Meta:
        db_table = 'questions'

