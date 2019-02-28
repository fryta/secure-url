from django.urls import path, re_path
from rest_framework.routers import DefaultRouter

from .views import SecuredEntityStatsApiView, SecuredEntityCreateListRetrieveApiViewSet, \
    SecuredEntityRegeneratePasswordApiView

app_name = 'secure_url.api'

urlpatterns = [
    path('stats/', SecuredEntityStatsApiView.as_view(), name='secured-entity-stats-api-view'),
    re_path(r'^regenerate-password/(?P<pk>[a-zA-Z0-9-]{36})/?$', SecuredEntityRegeneratePasswordApiView.as_view(),
            name='secured-entity-regenerate-password-api-view'),
]

secured_entity_api_router = DefaultRouter()
secured_entity_api_router.register(r'', SecuredEntityCreateListRetrieveApiViewSet, basename='secured-entity')
urlpatterns += secured_entity_api_router.urls
