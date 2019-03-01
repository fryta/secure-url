from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


def validate_access_to_secured_entity(data, secured_entity):
    if data['password'] != secured_entity.password:
        raise ValidationError({'password': _('Password do not match.')})

    if not secured_entity.is_accessible:
        raise ValidationError(_('Sorry, this secured entity is no longer available.'))

    return data

def validate_secured_entity(data):
    if not data.get('url') and not data.get('file'):
        raise ValidationError(_('You have to provide either url or file.'))

    if data.get('url') and data.get('file'):
        raise ValidationError(_('You can\'t provide both url or file.'))

    return data
