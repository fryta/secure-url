from django.urls import path, re_path

from .views import SecuredEntityStatsApiView

app_name = 'secure_url.api'

urlpatterns = [
    path('stats/', SecuredEntityStatsApiView.as_view(), name='secured-entity-stats-api-view'),
]
