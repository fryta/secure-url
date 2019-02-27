from django.shortcuts import get_object_or_404
from django.urls.base import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin

from .forms import SecuredEntityAccessForm
from .models import SecuredEntity


class SecuredEntityCreateView(LoginRequiredMixin, CreateView):
    model = SecuredEntity
    fields = ['url', 'file']

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.instance.user = self.request.user
        return form

    def get_success_url(self):
        return '{}?created=1'.format(super().get_success_url())


class SecuredEntityDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = SecuredEntity

    def test_func(self):
        return self.get_object().user.pk == self.request.user.pk

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['url'] = self.request.build_absolute_uri(
            reverse('secure_url:secured-entity-access-view', args=(self.object.pk,)))
        return context


class SecuredEntityAccessView(FormView):
    form_class = SecuredEntityAccessForm
    template_name = 'secure_url/securedentity_access.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = get_object_or_404(SecuredEntity, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['object'] = self.object
        return context_data

    def get_success_url(self):
        return self.object.get_redirect_url()
