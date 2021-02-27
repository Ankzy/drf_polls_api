from rest_framework import serializers
from .models import Poll, Answer, Question, Option
from .custom_validators import question_already_answered, more_than_one_answer_to_same, different_users, \
    choice_custom_validator, poll_question_conformity

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

        already_answered = question_already_answered(validated_data)
        if already_answered is not False:
            raise serializers.ValidationError({'error': 'User {} already answered question {}'.format(
                already_answered[0], already_answered[1])})

        if different_users(self.context):
            raise serializers.ValidationError({'error': 'Answers from different users in one request'})

        if more_than_one_answer_to_same(self.context):
            raise serializers.ValidationError({'error': 'More than one answer to the same question'})

        question_conformity = poll_question_conformity(self.context)
        if question_conformity is not False:
            raise serializers.ValidationError(question_conformity)

        choice_valid = choice_custom_validator(self.context)
        if choice_valid is not False:
            raise serializers.ValidationError(choice_valid)


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



