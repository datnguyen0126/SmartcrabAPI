from rest_framework import routers
from .views import QuestionViewSet

app_name = 'api_question'

router = routers.DefaultRouter(trailing_slash=False)
router.register('', QuestionViewSet, basename='question')

urlpatterns = router.urls
