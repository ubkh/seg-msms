from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView, ListView, UpdateView
from django.views.generic import FormView

from lessons.forms import SchoolCreateForm
from lessons.forms import SchoolManageForm
from lessons.models import School
from lessons.views.mixins import GroupRestrictedMixin, SchoolGroupRestrictedMixin
from lessons.views.mixins import SchoolObjectMixin


class HomeView(LoginRequiredMixin, ListView):
    model = School
    template_name = "school/list_school.html"
    context_object_name = "schools"


class SchoolHomeView(LoginRequiredMixin, SchoolObjectMixin, FormView):
    model = School
    template_name = "school/home.html"
    pk_url_kwarg = 'school'
    http_method_names = ['get', 'post']
    form_class = forms.Form

    def form_valid(self, form):
        school = School.objects.get(id=self.school_id)
        if school.is_director(self.request.user):
            return self.handle_no_permission()
        if form.data['follow']:
            school.set_group_client(self.request.user)
        else:
            school.leave_school(self.request.user)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('school_home', kwargs={'school': self.school_id})


class SchoolCreateView(GroupRestrictedMixin, CreateView):
    model = School
    template_name = "school/create_school.html"
    form_class = SchoolCreateForm
    http_method_names = ['get', 'post']
    allowed_group = "Director"

    def form_valid(self, form):
        form.instance.director = self.request.user
        school = form.save()
        school.set_group_director(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('home')


class SchoolManageView(SchoolGroupRestrictedMixin, SchoolObjectMixin, UpdateView):
    model = School
    template_name = "school/manage_school.html"
    form_class = SchoolManageForm
    pk_url_kwarg = 'school'
    http_method_names = ['get', 'post']
    allowed_group = "Director"

    def form_valid(self, form):
        school = form.save()
        if form.data.get('delete_school'):
            school.delete()
            return HttpResponseRedirect(reverse('home'))
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('school_home', kwargs={'school': self.school_id})
