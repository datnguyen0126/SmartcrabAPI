from django.db import models

from api_questions.models import Answers


class Reply(models.Model):
    content = models.TextField(blank=True, null=True)
    answer = models.ForeignKey(Answers, related_name='option', on_delete=models.CASCADE)
    answer_content = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'reply'

