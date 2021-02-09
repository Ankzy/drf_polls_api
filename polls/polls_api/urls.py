from django.urls import path
from .views import PollsView, AnswersView



urlpatterns = [
    path('polls/', PollsView.as_view()),
    path('answers/<int:pk>', AnswersView.as_view())
]