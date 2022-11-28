from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def display_children(request):
    return render(request, "children/children.html", )
