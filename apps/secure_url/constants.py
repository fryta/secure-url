from django.utils.translation import gettext as _


class SecuredEntityTypes(object):
    LINK = 'links'
    FILE = 'files'

    @classmethod
    def get_choices(cls):
        return (
            (cls.LINK, _("Link")),
            (cls.FILE, _("File"))
        )
