from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import SecuredEntityStatsApiView, SecuredEntityCreateListRetrieveApiViewSet

app_name = 'secure_url.api'

urlpatterns = [
    path('stats/', SecuredEntityStatsApiView.as_view(), name='secured-entity-stats-api-view'),
]

secured_entity_api_router = DefaultRouter()
secured_entity_api_router.register(r'', SecuredEntityCreateListRetrieveApiViewSet, basename='securedentity')
urlpatterns += secured_entity_api_router.urls
