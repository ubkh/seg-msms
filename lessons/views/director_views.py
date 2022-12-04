from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView

from lessons.forms import RegisterForm
from lessons.models import User
from lessons.views import GroupRestrictedMixin


class DirectorCreateView(LoginRequiredMixin, GroupRestrictedMixin, CreateView):
    model = User
    template_name = "authentication/register.html"
    form_class = RegisterForm
    http_method_names = ['get', 'post']
    allowed_group = "System-administrator"

    def form_valid(self, form):
        director = form.save()
        director.set_group_director()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('home')

    def handle_no_permission(self):
        return redirect('home')