from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class UserAgentWatchdogConfig(AppConfig):
    name = 'user_agent_watchdog'
    verbose_name = _("User Agent Watchdog")
