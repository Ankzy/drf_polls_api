from rest_framework.routers import DefaultRouter
from .views import PollsView, CompletedPollsView, AnswersView



router = DefaultRouter()
router.register(r'polls', PollsView, 'Polls')
router.register(r'completed-polls', CompletedPollsView, 'CompletedPolls')
router.register(r'answers', AnswersView, 'Answers')

urlpatterns = router.urls
