from rest_framework import serializers

from api_questions.serializers import AnswerSerializers
from api_result.models import ClusteringScores, TrainData, Reply


class ClusterScoreSerializers(serializers.ModelSerializer):

    class Meta:
        model = ClusteringScores
        fields = '__all__'


class ClusterQuestionSerializers(serializers.ModelSerializer):

    class Meta:
        model = TrainData
        fields = '__all__'
