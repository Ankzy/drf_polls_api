from rest_framework.response import Response
from rest_framework import viewsets
from .models import Poll, Answer
from .serializers import PollSerializer, PostAnswerSerializer, CompletedPollSerializer
import pytz
import datetime


class PollsView(viewsets.ViewSet):
    def list(self, request):
        now = pytz.UTC.localize(datetime.datetime.now())
        active_polls = Poll.objects.filter(end_datetime__gt=now)
        serializer = PollSerializer(active_polls, many=True)
        return Response(serializer.data)



class AnswersView(viewsets.ViewSet):
    def create(self, request):
        data = request.data
        serializer = PostAnswerSerializer(data=data, many=True, context=data)
        if serializer.is_valid(raise_exception=True):
            serializer.create(data)
        return Response({'status': 'Answers were created'})



class CompletedPollsView(viewsets.ViewSet):
    def retrieve(self, request, pk):
        user_polls_ids = set()
        for answer in Answer.objects.filter(user=pk):
            user_polls_ids.add(answer.poll.id)
        user_polls = Poll.objects.filter(id__in=user_polls_ids)
        serializer = CompletedPollSerializer(user_polls, many=True, context={'user': pk})
        return Response(serializer.data)

