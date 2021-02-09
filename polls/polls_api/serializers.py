from rest_framework import serializers
from .models import Poll, Answer, Question, Option


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ('id', 'text')

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)

    class Meta:
        model = Question
        fields = ('id', 'title', 'type', 'options')

class PollSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Poll
        fields = ('id', 'title', 'start_datetime', 'end_datetime', 'description', 'questions')

class PostAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('user', 'poll', 'question', 'choice_id', 'text')

    def create(self, validated_data):
        user = validated_data['user']
        poll = Poll.objects.get(id=validated_data['poll'])
        question = Question.objects.get(id=validated_data['question'])
        text = validated_data['text']

        if question.type == "MULT":
            answers = []
            for choice in validated_data['choice_id']:
                valid_choice = Option.objects.get(id=choice)
                answers.append(Answer(user=user, poll=poll, question=question, choice=valid_choice))
            return Answer.objects.bulk_create(answers)

        if question.type == "SNGL":
            valid_choice = Option.objects.get(id=validated_data['choice_id'])
            return Answer.objects.create(user=user, poll=poll, question=question, choice=valid_choice)

        Answer.objects.create(user=user, poll=poll, question=question, text=text)



class CompletedAnswerSerializer(serializers.ModelSerializer):
    choice = OptionSerializer()

    class Meta:
        model = Answer
        fields = ('user', 'text', 'choice')

class CompletedQuestionSerializer(serializers.ModelSerializer):
    completed_answer = serializers.SerializerMethodField('answer_serializer')

    def answer_serializer(self, obj):
        return CompletedAnswerSerializer(Answer.objects.filter(question__id=obj.id, user=self.context['user']), many=True).data

    class Meta:
        model = Question
        fields = ('title', 'type', 'completed_answer')


class CompletedPollSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField('question_serializer')

    def question_serializer(self, obj):
        return CompletedQuestionSerializer(Question.objects.filter(poll__id=obj.id), context=self.context, many=True).data

    class Meta:
        model = Poll
        fields = ('id', 'title', 'start_datetime', 'end_datetime', 'description', 'questions')



