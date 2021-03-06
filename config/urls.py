"""settings URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.views.generic.base import TemplateView
from rest_framework_swagger.views import get_swagger_view

api_schema_view = get_swagger_view(title='Secure URL - API')

urlpatterns = [
    path('api/secure-url/', include('apps.secure_url.api.urls')),
    path('api/', api_schema_view),

    path('secure-url/', include('apps.secure_url.urls')),

    path('login/',
         auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name='static/login.html'),
         name='accounts-login'),
    path('logout/', auth_views.LogoutView.as_view(), name='accounts-logout'),

    path('admin/', admin.site.urls),

    path('', login_required(TemplateView.as_view(template_name='static/home.html')), name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
