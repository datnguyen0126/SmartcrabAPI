from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('data/', include('api_data.urls')),
    path('question/', include('api_questions.urls')),
    path('result/', include('api_result.urls'))
]
