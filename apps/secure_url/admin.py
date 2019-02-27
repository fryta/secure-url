from django.contrib import admin
from django.urls.base import reverse
from django.utils.safestring import mark_safe

from .actions import regenerate_passwords
from .models import SecuredEntity


@admin.register(SecuredEntity)
class SecuredEntityAdmin(admin.ModelAdmin):
    list_display = ('user', 'created', 'is_accessible')
    list_filter = ('user', 'created')
    actions = (regenerate_passwords,)
    fields = ('user', 'url', 'file', 'password', 'secure_url', 'created')
    readonly_fields = ('user', 'url', 'file', 'password', 'secure_url', 'created')

    @mark_safe
    def secure_url(self, obj):
        return '<a href="{secure_url}" target="_blank">{secure_url}</a>'.format(
            secure_url=reverse('secure_url:secured-entity-access-view', args=(obj.pk,)))
