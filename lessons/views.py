"""
Views that will be used in the music school management system.
"""

from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404

from lessons.models import Lesson, User
from .forms import LessonModifyForm, LessonRequestForm, RegisterForm
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from lessons.helpers import login_prohibited, director_required

# Create your views here.
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
            student_group, created = Group.objects.get_or_create(name='Student')
            user.groups.add(student_group)
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

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
    return render(request, "login.html", {'form': form, 'next': next})

def log_out(request):
    logout(request)
    return redirect('index')

@login_required
def request_lesson(request):
    """
    View that displays the form allowing users to request a lesson.
    If the form is valid, the user is redirected to the home page and 
    a Lesson object is created.
    """
    if request.method == "POST":
        form = LessonRequestForm(request.POST)
        if form.is_valid():
            form.instance.student = request.user
            form.save()
            return redirect('home')
    form = LessonRequestForm()
    return render(request, "lessons/request_lesson.html", {'form': form})

@login_required
def modify_lesson(request, pk):
    """
    View that displays the form allowing users to edit an existing lesson
    request. If the form is valid, the user is redirected to the home page
    and the corresponding Lesson object updated.
    """
    data = get_object_or_404(Lesson, id=pk)
    form = LessonModifyForm(instance=data)

    if request.method == "POST":
        form = LessonModifyForm(request.POST, instance=data)

        if form.is_valid():
            if request.user == form.instance.student:
                form.instance.student = request.user
                form.save()
                return redirect('home')
    return render(request, "lessons/modify_lesson.html", {'form': form})

@login_required
def home(request):
    """
    View that displays the user's home page.
    """
    lessons = Lesson.objects.filter(student=request.user).order_by('-fulfilled')
    administrators = User.objects.filter(groups__name='Administrator')

    return render(request, "home.html", {'lessons' : lessons, 'administrators' : administrators})


@login_required
@director_required
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
    return render(request, 'register.html', {'form': form})