from django.contrib import admin

from .models import UserAgentLog


@admin.register(UserAgentLog)
class UserAgentLogAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
