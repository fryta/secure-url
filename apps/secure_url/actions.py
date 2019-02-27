from django.utils.translation import gettext as _

def regenerate_passwords(modeladmin, request, queryset):
    for obj in queryset.all():
        obj.regenerate_password()

    modeladmin.message_user(request, _('Passwords have been regenerated for %(count)s secured entities.') %
                            {'count': queryset.count()})
