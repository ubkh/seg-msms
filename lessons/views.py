"""
Views that will be used in the music school management system.
"""

from django.shortcuts import render, redirect
from .forms import RegisterForm
from .forms import LoginForm
from django.contrib.auth import authenticate, login

# Create your views here.

def index(request):
    """
    View that displays the index page.
    """
    return render(request, "index.html")

def register(request):
    """
    View that displays the registration page and registration forms. If a valid 
    form is submitted the user is redirected to the home page, else they are 
    directed to resubmit the form again.
    """
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'register.html', {'form': form})

def log_in(request):
    """
    View that displays the login page.
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
    form = LoginForm()
    return render(request, "login.html", {'form': form})

def home(request):
    """
    View that displays the user's home page.
    """
    return render(request, "home.html")
