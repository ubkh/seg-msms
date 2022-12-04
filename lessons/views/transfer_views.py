"""
Views that will be used in the music school management system.
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView

from lessons.forms import TransferForm
from lessons.models import Transfer, Lesson, User
from lessons.views.mixins import GroupRestrictedMixin, SchoolObjectMixin, SchoolGroupRestrictedMixin


class TransferListView(LoginRequiredMixin, SchoolGroupRestrictedMixin, SchoolObjectMixin, ListView):

    model = Transfer
    template_name = "transfer/transfers.html"
    context_object_name = "transfers"
    allowed_group = "Administrator"

    def handle_no_permission(self):
        return redirect('home')


class TransferCreateView(LoginRequiredMixin, SchoolGroupRestrictedMixin, SchoolObjectMixin, CreateView):

    model = Transfer
    template_name = "transfer/record_transfer.html"
    form_class = TransferForm
    http_method_names = ['get', 'post']
    allowed_group = "Administrator"

    def get_form_kwargs(self):
        kwargs = super(TransferCreateView, self).get_form_kwargs()
        kwargs['school'] = self.kwargs['school']
        return kwargs

    def form_valid(self, form):
        form.instance.user = User.objects.filter(pk=form.cleaned_data.get('user_id')).first()
        form.instance.lesson = Lesson.objects.filter(pk=form.cleaned_data.get('lesson_id')).first()
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('transfers', kwargs={'school': self.kwargs['school']})

    def handle_no_permission(self):
        return redirect('home')
