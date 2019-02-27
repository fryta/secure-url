from django.urls import path, re_path

from .views import SecuredEntityCreateView, SecuredEntityDetailView

app_name = 'secure_url'

urlpatterns = [
    re_path(r'^secured-entity/(?P<pk>[a-zA-Z0-9-]{36})/?$', SecuredEntityDetailView.as_view(),
            name='secured-entity-detail-view'),
    path('secured-entity/create/', SecuredEntityCreateView.as_view(), name='secured-entity-create-view'),
]
