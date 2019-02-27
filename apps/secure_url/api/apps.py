from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ApiConfig(AppConfig):
    name = 'secure_url.api'
    verbose_name = _("Secure URL - API")
