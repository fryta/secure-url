from django.urls import path, re_path

from .views import SecuredEntityCreateView, SecuredEntityDetailView, SecuredEntityListView, \
    SecuredEntityAccessView

app_name = 'secure_url'

urlpatterns = [
    re_path(r'^(?P<pk>[a-zA-Z0-9-]{36})/?$', SecuredEntityDetailView.as_view(),
            name='secured-entity-detail-view'),
    re_path(r'^get-access/(?P<pk>[a-zA-Z0-9-]{36})/?$', SecuredEntityAccessView.as_view(),
            name='secured-entity-access-view'),
    path('create/', SecuredEntityCreateView.as_view(), name='secured-entity-create-view'),
    path('', SecuredEntityListView.as_view(), name='secured-entity-list-view'),
]
