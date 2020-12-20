from rest_framework import routers
from .views import DataViewSet

app_name = 'api_data'

router = routers.DefaultRouter(trailing_slash=False)
router.register('', DataViewSet, basename='data')

urlpatterns = router.urls
