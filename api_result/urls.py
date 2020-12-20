from rest_framework import routers
from .views import ResultViewSet, ReplyViewSet

app_name = 'api_result'

router = routers.DefaultRouter(trailing_slash=False)
router.register('', ResultViewSet, basename='result')
router.register('reply', ReplyViewSet, basename='reply')

urlpatterns = router.urls
