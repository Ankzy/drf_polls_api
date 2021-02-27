from django.db import models


class Poll(models.Model):
    title = models.CharField(max_length=120)
    start_datetime = models.DateTimeField(auto_now_add=True)
    end_datetime = models.DateTimeField()
    description = models.TextField()

    def __str__(self):
        return self.title


class Question(models.Model):
    text_question = 'TEXT'
    single_choice = 'SNGL'
    multiple_choice = 'MULT'
    question_type_choices = (
        (text_question, 'Text question'),
        (single_choice, 'Single-choice question'),
        (multiple_choice, 'Multiple-choice question')
    )

    title = models.CharField(max_length=500)
    type = models.CharField(max_length=4, choices=question_type_choices)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.title


class Option(models.Model):
    text = models.CharField(max_length=200)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')

    def __str__(self):
        return self.text


class Answer(models.Model):
    user = models.IntegerField()
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='completed_answer')
    choice = models.ForeignKey(Option, blank=True, null=True, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        unique_together = ('user', 'choice', 'question')

