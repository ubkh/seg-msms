from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView

from lessons.forms import RegisterForm
from lessons.models import User
from lessons.views import GroupRestrictedMixin


class DirectorCreateView(GroupRestrictedMixin, CreateView):
    """
    View that displays the create director page and forms.
    If a valid form is submitted the user is redirected to the home page.
    """

    model = User
    template_name = "authentication/create_director.html"
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
