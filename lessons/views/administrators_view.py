"""
Views that will be used in the music school management system.
"""

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView

from lessons.forms import RegisterForm, AdminModifyForm, BanClientForm
from lessons.helpers import super_administrator_restricted
from lessons.mixins import GroupRestrictedMixin
from lessons.models import User


class AdministratorListView(LoginRequiredMixin, GroupRestrictedMixin, ListView):
    """

    """

    model = User
    template_name = "administrators/administrators.html"
    context_object_name = "administrators"
    allowed_group = "Super-administrator"

    def get_queryset(self):
        return User.objects.filter(groups__name='Administrator')

    def handle_no_permission(self):
        return redirect('home')


class AdministratorCreateView(LoginRequiredMixin, GroupRestrictedMixin, CreateView):
    """
    View that displays the form to register an administrator. If a valid
    form is submitted the director is redirected to the home page, else they are
    directed to resubmit the form again.
    """

    model = User
    template_name = "authentication/register.html"
    form_class = RegisterForm
    http_method_names = ['get', 'post']
    allowed_group = "Super-administrator"

    def form_valid(self, form):
        administrator = form.save()
        administrator.set_group_administrator()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('administrators')

    def handle_no_permission(self):
        return redirect('home')


class AdministratorUpdateView(LoginRequiredMixin, GroupRestrictedMixin, UpdateView):
    """
    View that displays the form to edit an administrator. If a valid
    form is submitted the director is redirected to the home page, else they are
    directed to resubmit the form again.
    """
    model = User
    template_name = "authentication/register.html"
    form_class = AdminModifyForm
    http_method_names = ['get', 'post']
    allowed_group = "Super-administrator"

    def form_valid(self, form):
        user = form.save()
        if form.data.get('make_account_super_administrator'):
            user.groups.clear()
            user.set_group_super_administrator()
        if form.data.get('delete_account'):
            user.delete()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('administrators')


@login_required
@super_administrator_restricted
def ban_client(request, pk):
    """"
    View used to ban clients
    """
    user = get_object_or_404(User, id=pk)
    form = BanClientForm(instance=user)

    if request.method == "POST":
        form = BanClientForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request, "authentication/ban_client.html", {'form': form})