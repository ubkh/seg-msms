"""
Views that will be used in the music school management system.
"""

from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404

from lessons.models import Lesson, User
from .forms import LessonRequestForm, RegisterForm
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView

# Create your views here.

def index(request):
    """
    View that displays the index page.
    """
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))
    return render(request, "index.html")

def register(request):
    """
    View that displays the registration page and registration forms. If a valid 
    form is submitted the user is redirected to the home page, else they are 
    directed to resubmit the form again.
    """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def log_in(request):
    """
    View that displays the login page and login forms. If a valid 
    form is submitted the user is redirected to the home page, else they are 
    directed to resubmit the form again.
    """
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
    return render(request, "login.html", {'form': form})

def log_out(request):
    logout(request)
    return redirect('index')

@login_required
def request_lesson(request):
    if request.method == "POST":
        form = LessonRequestForm(request.POST)
        if form.is_valid():
            form.instance.student = request.user
            form.save()
    form = LessonRequestForm()
    return render(request, "lessons/request_lesson.html", {'form': form})

@login_required
def home(request):
    """
    View that displays the user's home page.
    """
    lessons = Lesson.objects.filter(student=request.user).order_by('-fulfilled')

    return render(request, "home.html", {'lessons' : lessons})
