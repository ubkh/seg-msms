"""
Views that will be used in the music school management system.
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from lessons.models import User


@login_required
def administrators(request):
    administrator_list = User.objects.filter(groups__name='Administrator')
    return render(request, "home/administrators.html", {'administrators': administrator_list})
