from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SecureUrlConfig(AppConfig):
    name = 'secure_url'
    verbose_name = _("Secure URL")
