from api_questions.models import Questions, Answers
from api_questions.constants.questions import Questions as QuestionConst


class QuestionServices:

    @classmethod
    def initialize_question(cls):
        Questions.objects.filter(id__gte=-1).delete()
        Answers.objects.filter(id__gt=-1).delete()
        cls.load_questions()
        cls.load_options()

    @classmethod
    def load_questions(cls):
        i = 0
        for question in QuestionConst.QUESTIONS:
            Questions.objects.create(id=i, content=question.get('content'),\
                                          required=question.get('required'), multiple=question.get('multiple'),\
                                          spec=question.get('spec'), train=question.get('train'))
            i = i + 1

    @classmethod
    def load_options(cls):
        i = 0
        j = 0
        for question in QuestionConst.QUESTIONS:
            question1 = Questions.objects.get(pk=i)
            for option in question.get('options'):
                Answers.objects.create(id=j, content=option, question=question1)
                j = j + 1
            i = i + 1
