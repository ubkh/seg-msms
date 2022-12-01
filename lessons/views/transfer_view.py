"""
Views that will be used in the music school management system.
"""

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView

from lessons.forms import TransferForm
from lessons.models import Transfer
from lessons.helpers import administrator_restricted


# @administrator_restricted
class TransferListView(LoginRequiredMixin, ListView):

    model = Transfer
    template_name = "transfer/transfers.html"
    context_object_name = "transfers"


# @administrator_restricted
class TransferCreateView(LoginRequiredMixin, CreateView):

    model = Transfer
    template_name = "transfer/record_transfer.html"
    form_class = TransferForm
    http_method_names = ['get', 'post']

    def get_success_url(self):
        return reverse('transfers')

    def handle_no_permission(self):
        return redirect('home')
