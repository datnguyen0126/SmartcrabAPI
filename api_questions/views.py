from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api_questions.models import Questions, Answers
from api_questions.serializers import AnswerSerializers, QuestionSerializers
from api_questions.services import QuestionServices


class QuestionViewSet(viewsets.GenericViewSet):
    queryset = Questions.objects.select_related('answers')
    serializer_class = QuestionSerializers
    permission_classes = [AllowAny, ]

    def list(self, request):
        question = Questions.objects.all()
        question_serializer = self.get_serializer(question, many=True)
        return Response(question_serializer.data)

    def retrieve(self, request, *args, **kwargs):
        question = Questions.objects.filter(id=kwargs.get('pk')).first()
        question_serializer = self.get_serializer(question)
        return Response(question_serializer.data)

    @action(methods=['PUT'], detail=False)
    def initialize(self, request):
        QuestionServices.initialize_question()
        data = { 'success': True }
        return Response(data)

    @action(methods=['GET'], detail=False)
    def ai_question(self, request):
        question = Questions.objects.filter(train=1)
        question_serializer = self.get_serializer(question, many=True)
        return Response(question_serializer.data)

    def create(self, request):
        pass

    def update(self, request):
        pass

    def destroy(self, request):
        pass

