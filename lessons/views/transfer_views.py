"""
Views that will be used in the music school management system.
"""
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView

from lessons.forms import TransferForm
from lessons.models import Transfer, Lesson, User
from lessons.views.mixins import SchoolObjectMixin, SchoolGroupRestrictedMixin


class TransactionsListView(SchoolGroupRestrictedMixin, SchoolObjectMixin, ListView):
    """ 
    View that displays all user transactions to the user and their payment status.
    """

    model = Transfer
    template_name = "transfer/client_transfers.html"
    context_object_name = "transfers"
    allowed_group = "Client"

    def get_queryset(self):
        return super().get_queryset().filter(school=self.kwargs['school'])

    def get_context_data(self, **kwargs):
        context = super(TransactionsListView, self).get_context_data(**kwargs)
        context['transfers'] = Transfer.objects.filter(user_id=self.request.user).filter(school=self.kwargs['school'])
        return context

    def handle_no_permission(self):
        return redirect('home')


class SchoolTransferListView(SchoolGroupRestrictedMixin, SchoolObjectMixin, ListView):
    """ 
    View that displays all user transactions and their payment status to an administrator.
    """

    model = Transfer
    template_name = "transfer/transfers.html"
    context_object_name = "transfers"
    allowed_group = "Administrator"

    def get_queryset(self):
        return super().get_queryset().filter(school=self.kwargs['school'])

    def handle_no_permission(self):
        return redirect('home')


class TransferCreateView(SchoolGroupRestrictedMixin, SchoolObjectMixin, CreateView):
    """ 
    View that displays the create transaction form to an administrator.
    """

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
        return reverse('school_transfers', kwargs={'school': self.kwargs['school']})

    def handle_no_permission(self):
        return redirect('home')
