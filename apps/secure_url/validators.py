from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


def validate_secured_entity(data, secured_entity):
    if data['password'] != secured_entity.password:
        raise ValidationError({'password': _('Password do not match.')})

    if not secured_entity.is_accessible:
        raise ValidationError(_('Sorry, this secured entity is no longer available.'))
