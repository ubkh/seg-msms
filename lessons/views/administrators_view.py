"""
Views that will be used in the music school management system.
"""
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, get_object_or_404

from lessons.forms import RegisterForm, AdminModifyForm
from lessons.helpers import super_administrator_restricted
from lessons.models import User


@login_required
def display_administrators(request):
    administrator_list = User.objects.filter(groups__name='Administrator')
    return render(request, "administrators/administrators.html", {'administrators': administrator_list})


@login_required
@super_administrator_restricted
def create_administrator(request):
    """
    View that displays the form to register an administrator. If a valid
    form is submitted the director is redirected to the home page, else they are
    directed to resubmit the form again.
    """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            administrator_group, created = Group.objects.get_or_create(name='Administrator')
            user.groups.add(administrator_group)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'authentication/register.html', {'form': form})


@login_required
@super_administrator_restricted
def modify_administrator(request, pk):
    """
    View that displays the form to edit an administrator. If a valid
    form is submitted the director is redirected to the home page, else they are
    directed to resubmit the form again.
    """
    admin_data = get_object_or_404(User, id=pk)
    form = AdminModifyForm(instance=admin_data)
    if request.method == "POST":
        form = AdminModifyForm(request.POST, instance=admin_data)
        if form.is_valid():
            user = form.save()
            if form.data.get('make_account_director'):
                user.groups.clear()
                director_group, created = Group.objects.get_or_create(name='Director')
                user.groups.add(director_group)
            if form.data.get('delete_account'):
                user.delete()
            return redirect('home')
    return render(request, "authentication/register.html", {'form': form})
