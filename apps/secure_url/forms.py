from django import forms

from .models import SecuredEntity
from .validators import validate_secured_entity


class SecuredEntityAccessForm(forms.Form):
    password = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()
        secured_entity = SecuredEntity.objects.get(pk=self.data['id'])

        validate_secured_entity(self.cleaned_data, secured_entity)

        return cleaned_data
