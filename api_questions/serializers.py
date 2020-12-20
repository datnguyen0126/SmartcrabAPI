from rest_framework import serializers
from api_questions.models import Questions, Answers


class AnswerSerializers(serializers.ModelSerializer):

    class Meta:
        model = Answers
        fields = '__all__'


class QuestionSerializers(serializers.ModelSerializer):
    answers = AnswerSerializers(many=True, source='question')

    class Meta:
        model = Questions
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        return ret

