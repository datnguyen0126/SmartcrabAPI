from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action

from api_questions.models import Answers
from api_result.models import Reply


class ReplyViewSet(viewsets.GenericViewSet):

    permission_classes = [AllowAny, ]

    @action(methods=['POST'], detail=False)
    def get(self, request):
        answer = request.data.get('answer')
        reply = Reply.objects.filter(answer__content=answer).first()
        if reply:
            ret = dict(
                id=reply.id,
                content=reply.content,
                answer=reply.answer.content
            )
        else:
            ret = {}
        return Response(ret, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    def add(self, request):
        answers = request.data.get('answers')
        reply = answers
        if not reply:
            data = { 'success': True }
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_200_OK)

    @action(methods=['PUT'], detail=False)
    def edit(self, request):
        answer = request.data.get('answer')
        content = request.data.get('content')
        reply = Reply.objects.filter(answer__content=answer).first()
        if not reply:
            answer1 = Answers.objects.filter(content=answer).first()
            Reply.objects.create(content=content, answer=answer1)
            return Response(status=status.HTTP_200_OK)
        reply.content = content
        reply.save()
        return Response(status=status.HTTP_200_OK)

    @action(methods=['DELETE'], detail=True)
    def remove(self, request):
        answer_id = request.data.get('answer_id')
        Reply.objects.select_related('answer').filter(answer__id=answer_id).delete()
        data = { 'success': True }
        return Response(data, status=status.HTTP_200_OK)