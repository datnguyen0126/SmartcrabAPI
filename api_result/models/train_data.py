from django.db import models

from api_data.models import Laptop
from api_questions.models import Answers


class TrainData(models.Model):
    laptop_name = models.CharField(max_length=255, blank=True, null=True)
    answer_name = models.CharField(max_length=255, blank=True, null=True)
    training = models.BooleanField(default=False)

    # related files if needed
    laptop = models.ForeignKey(Laptop, related_name='result', on_delete=models.CASCADE)
    answer = models.ForeignKey(Answers, on_delete=models.CASCADE, related_name='answer', null=True, blank=True)
    check = models.BooleanField(default=False)

    class Meta:
        db_table = 'train_data'

