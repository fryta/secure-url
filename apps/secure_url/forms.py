from django import forms

from .models import SecuredEntity
from .validators import validate_access_to_secured_entity, validate_secured_entity


class SecuredEntityForm(forms.ModelForm):

    def clean(self):
        return validate_secured_entity(self.cleaned_data)

    class Meta:
        model = SecuredEntity
        fields = ['url', 'file']


class SecuredEntityAccessForm(forms.Form):
    password = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()
        secured_entity = SecuredEntity.objects.get(pk=self.data['id'])

        return validate_access_to_secured_entity(cleaned_data, secured_entity)
