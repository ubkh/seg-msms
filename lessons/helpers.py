from django.shortcuts import redirect
from msms.settings import LOGGED_IN_REDIRECT_URL

def login_prohibited(view_function):
    def modified_view_function(request):
        if request.user.is_authenticated:
            return redirect(LOGGED_IN_REDIRECT_URL)
        else:
            return view_function(request)
    return modified_view_function

def super_administrator_restricted(view_function):
    def modified_view_function(request, *args, **kwargs):
        if request.user.groups.filter(name='Director').exists():
            return view_function(request, *args, **kwargs)
        else:
            return redirect(LOGGED_IN_REDIRECT_URL)
    return modified_view_function