from django.db import models
from api_questions.models.questions import Questions


class Answers(models.Model):
    id = models.IntegerField(primary_key=True)
    content = models.CharField(max_length=255, blank=True, null=True)
    question = models.ForeignKey(Questions, related_name='question', on_delete=models.CASCADE)
    icon = models.CharField(max_length=255, blank=True, null=True)
    keyword = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'answers'