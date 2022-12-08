from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView

from lessons.forms import ChildCreateForm
from lessons.models import User
from lessons.views.mixins import GroupRestrictedMixin


class ChildListView(GroupRestrictedMixin, ListView):
    """
    View that displays a list of children to an adult user.
    """

    model = User
    template_name = "children/children.html"
    context_object_name = "children"
    allowed_group = "Adult-user"

    def get_queryset(self):
        return User.objects.filter(parent=self.request.user)

    def handle_no_permission(self):
        return redirect('home')


class ChildCreateView(GroupRestrictedMixin, CreateView):
    """
    View that displays the child registration page and form. If a valid 
    form is submitted the user is redirected to the children list page.
    """

    model = User
    template_name = "children/create_child.html"
    form_class = ChildCreateForm
    http_method_names = ['get', 'post']
    allowed_group = "Adult-user"

    def form_valid(self, form):
        child = form.save()
        child.parent = self.request.user
        child.save()
        child.set_group_user()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('children')

    def handle_no_permission(self):
        return redirect('home')
