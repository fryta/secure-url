from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin

from .models import SecuredEntity


class SecuredEntityCreateView(LoginRequiredMixin, CreateView):
    model = SecuredEntity
    fields = ['url', 'file']

    def get_form(self, *args, **kwargs):
        form = super(SecuredEntityCreateView, self).get_form(*args, **kwargs)
        form.instance.user = self.request.user
        return form


class SecuredEntityDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = SecuredEntity

    def test_func(self):
        return self.get_object().user.pk == self.request.user.pk
