from django.contrib import admin

from .models import SecuredEntity


@admin.register(SecuredEntity)
class SecuredEntityAdmin(admin.ModelAdmin):
    list_display = ('user', 'created')
