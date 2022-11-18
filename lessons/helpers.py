from django.shortcuts import redirect
from msms.settings import LOGGED_IN_REDIRECT_URL

def login_prohibited(view_function):
    def modified_view_function(request):
        if request.user.is_authenticated:
            return redirect(LOGGED_IN_REDIRECT_URL)
        else:
            return view_function(request)
    return modified_view_function

def director_required(view_function):
    def modified_view_function(request):
        if request.user.groups.filter(name='Director').exists():
            return view_function(request)
        else:
            return redirect(LOGGED_IN_REDIRECT_URL)
    return modified_view_function