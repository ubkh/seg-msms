"""
Views that will be used in the music school management system.
"""

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from lessons.forms import LoginForm
from lessons.forms import RegisterForm, EditUserForm
from lessons.helpers import login_prohibited
from lessons.models import User
from lessons.views.mixins import SchoolObjectMixin, SchoolGroupRestrictedMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView


@login_prohibited
def index(request):
    """ 
    View that displays the index page.
    """
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))
    return render(request, "index.html")


@login_prohibited
def register(request):
    """
    View that displays the registration page and registration forms. If a valid 
    form is submitted the user is redirected to the home page, else they are 
    directed to resubmit the form again.
    """
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_group_user()
            if form.data.get('make_account_adult_student'):
                user.set_group_adult_user()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'authentication/register.html', {'form': form})


@login_prohibited
def log_in(request):
    """
    View that displays the login page and login forms. If a valid 
    form is submitted the user is redirected to the home page, else they are 
    directed to resubmit the form again.
    """
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(name=name, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        # User inputs incorrect data
        messages.add_message(request, messages.ERROR, "Incorrect details")
    form = LoginForm()
    next = request.GET.get('next') or ''
    return render(request, "authentication/login.html", {'form': form, 'next': next})


def log_out(request):
    logout(request)
    return redirect('index')


class EditUserView(LoginRequiredMixin, SchoolGroupRestrictedMixin, SchoolObjectMixin, UpdateView):
    model = User
    template_name = "authentication/edit_profile.html"
    form_class = EditUserForm
    http_method_names = ['get', 'post']

    def form_valid(self, form):
        super().form_valid(form)
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('edit_profile', kwargs={'school': self.kwargs['school']})

    def handle_no_permission(self):
        return redirect('home')



