from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from .models import SecuredEntity


class SecuredEntityAccessForm(forms.Form):
    password = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()
        secured_entity = SecuredEntity.objects.get(pk=self.data['id'])

        if self.cleaned_data['password'] != secured_entity.password:
            raise ValidationError({'password': _('Password do not match.')})

        if not secured_entity.is_accessible:
            raise ValidationError(_('Sorry, this secured entity is no longer available.'))

        return cleaned_data
