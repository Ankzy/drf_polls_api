from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Poll, Answer
from .serializers import PollSerializer, PostAnswerSerializer, CompletedPollSerializer
from .custom_validators import question_already_answered, more_than_one_answer_to_same, different_users, \
    choice_custom_validator, poll_question_conformity
import pytz
import datetime


class PollsView(APIView):
    def get(self, request):
        now = pytz.UTC.localize(datetime.datetime.now())
        active_polls = Poll.objects.filter(end_datetime__gt=now)
        serializer = PollSerializer(active_polls, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        serializer = PostAnswerSerializer(data=data, many=True)
        if serializer.is_valid(raise_exception=True):

            already_answered = question_already_answered(data)
            if already_answered is not False:
                return Response({'error': 'User {} already answered question {}'.format(
                    already_answered[0], already_answered[1])})

            if different_users(data):
                return Response({'error': 'Answers from different users in one request'})

            if more_than_one_answer_to_same(data):
                return Response({'error': 'More than one answer to the same question'})

            question_conformity = poll_question_conformity(data)
            if question_conformity is not False:
                return Response(question_conformity)

            choice_valid = choice_custom_validator(data)
            if choice_valid is not False:
                return Response(choice_valid)

            serializer.create(data)
        return Response({'status': 'Answers were created'})



class AnswersView(APIView):
    def get(self, request, pk):
        user_polls_ids = set()
        for answer in Answer.objects.filter(user=pk):
            user_polls_ids.add(answer.poll.id)
        user_polls = Poll.objects.filter(id__in=user_polls_ids)
        serializer = CompletedPollSerializer(user_polls, many=True, context={'user': pk})
        return Response(serializer.data)

