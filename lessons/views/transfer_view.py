"""
Views that will be used in the music school management system.
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView

from lessons.forms import TransferForm
from lessons.mixins import GroupRestrictedMixin
from lessons.models import Transfer


class TransferListView(LoginRequiredMixin, GroupRestrictedMixin, ListView):

    model = Transfer
    template_name = "transfer/transfers.html"
    context_object_name = "transfers"
    allowed_group = "Administrator"

    def handle_no_permission(self):
        return redirect('home')


class TransferCreateView(LoginRequiredMixin, GroupRestrictedMixin, CreateView):

    model = Transfer
    template_name = "transfer/record_transfer.html"
    form_class = TransferForm
    http_method_names = ['get', 'post']
    allowed_group = "Administrator"

    def get_success_url(self):
        return reverse('transfers')

    def handle_no_permission(self):
        return redirect('home')
