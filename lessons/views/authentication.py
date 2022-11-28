"""
Views that will be used in the music school management system.
"""

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from lessons.forms import LoginForm
from lessons.forms import RegisterForm, AdminModifyForm
from lessons.helpers import login_prohibited, super_administrator_restricted
from lessons.models import Lesson, User, Transfer


@login_prohibited
def index(request):
    """ 
    View that displays the index page.
    """
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))
    return render(request, "index.html")


@login_required
def home(request):
    """
    View that displays the user's home page.
    """
    students = User.objects.filter(groups__name='Student')
    lessons = Lesson.objects.filter(student=request.user).order_by('-fulfilled')
    administrators = User.objects.filter(groups__name='Administrator')
    transfers = Transfer.objects.filter(user_id=request.user)

    return render(request, "home/home.html",
                  {'students': students, 'lessons': lessons, 'administrators': administrators, 'transfers': transfers})


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
            student_group, created = Group.objects.get_or_create(name='Student')
            user.groups.add(student_group)
            if form.data.get('make_account_adult_student'):
                adult_student_group, created = Group.objects.get_or_create(name='Adult-student')
                user.groups.add(adult_student_group)
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



