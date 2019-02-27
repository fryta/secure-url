from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls.base import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.views.generic.list import ListView

from ..forms import SecuredEntityAccessForm
from ..mixins import EditOnlyOwnSecuredEntitiesMixin
from ..models import SecuredEntity, SecuredEntityAccessLog


class SecuredEntityCreateView(LoginRequiredMixin, CreateView):
    model = SecuredEntity
    fields = ['url', 'file']

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.instance.user = self.request.user
        return form

    def get_success_url(self):
        return '{}?created=1'.format(super().get_success_url())


class SecuredEntityDetailView(LoginRequiredMixin, EditOnlyOwnSecuredEntitiesMixin, DetailView):
    model = SecuredEntity

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['url'] = self.request.build_absolute_uri(
            reverse('secure_url:secured-entity-access-view', args=(self.object.pk,)))
        return context


class SecuredEntityRegeneratePasswordView(LoginRequiredMixin, EditOnlyOwnSecuredEntitiesMixin, UpdateView):
    model = SecuredEntity
    fields = []

    def get(self, request, *args, **kwargs):
        secured_entity = get_object_or_404(SecuredEntity, pk=kwargs['pk'])
        return HttpResponseRedirect(secured_entity.get_absolute_url())

    def form_valid(self, form):
        self.object.regenerate_password()
        return super().form_valid(form)


class SecuredEntityListView(LoginRequiredMixin, ListView):
    model = SecuredEntity

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


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

    def form_valid(self, form):
        SecuredEntityAccessLog.objects.create(secured_entity=self.object)
        return super().form_valid(form)
