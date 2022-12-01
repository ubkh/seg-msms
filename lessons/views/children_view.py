from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView

from lessons.forms import ChildCreateForm
from lessons.mixins import GroupRestrictedMixin
from lessons.models import User


class ChildListView(LoginRequiredMixin, GroupRestrictedMixin, ListView):

    model = User
    template_name = "children/children.html"
    context_object_name = "children"
    allowed_group = "Adult-student"

    def get_queryset(self):
        return User.objects.filter(parent=self.request.user)

    def handle_no_permission(self):
        return redirect('home')


class ChildCreateView(LoginRequiredMixin, GroupRestrictedMixin, CreateView):

    model = User
    template_name = "authentication/register.html"
    form_class = ChildCreateForm
    http_method_names = ['get', 'post']
    allowed_group = "Adult-student"

    def form_valid(self, form):
        child = form.save()
        child.parent = self.request.user
        child.save()
        child.set_group_student()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('children')

    def handle_no_permission(self):
        return redirect('home')
