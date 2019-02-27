from django.contrib.auth.mixins import UserPassesTestMixin


class EditOnlyOwnSecuredEntitiesMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().user.pk == self.request.user.pk
