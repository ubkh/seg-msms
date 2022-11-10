"""
Views that will be used in the music school management system.
"""

from django.shortcuts import render, redirect
from .forms import RegisterForm
from .forms import LoginForm

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

def login(request):
    """
    View that displays the login page.
    """
    form = LoginForm()
    return render(request, "login.html", {'form': form})

def home(request):
    """
    View that displays the user's home page.
    """
    return render(request, "home.html")
