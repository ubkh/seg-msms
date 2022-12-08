from django.shortcuts import redirect
from msms.settings import LOGGED_IN_REDIRECT_URL
from lessons.models import Lesson


def login_prohibited(view_function):
    def modified_view_function(request):
        if request.user.is_authenticated:
            return redirect(LOGGED_IN_REDIRECT_URL)
        else:
            return view_function(request)

    return modified_view_function


def lesson_fulfilled_restricted(view_function):
    def modified_view_function(request, *args, **kwargs):
        lesson = Lesson.objects.get(pk=kwargs['pk'])
        if lesson.fulfilled:
            return view_function(request, *args, **kwargs)
        else:
            return redirect(LOGGED_IN_REDIRECT_URL)

    return modified_view_function
