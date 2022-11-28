from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect

from lessons.forms import ChildCreateForm
from lessons.models import User


@login_required
def display_children(request):
    children_list = User.objects.filter(parent=request.user)
    return render(request, "children/children.html", {'children': children_list})


@login_required
def create_child(request):
    if request.method == "POST":
        form = ChildCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.parent = request.user
            user.save()
            student_group, created = Group.objects.get_or_create(name='Student')
            user.groups.add(student_group)
            return redirect('children')
    else:
        form = ChildCreateForm()
    return render(request, 'authentication/register.html', {'form': form})
