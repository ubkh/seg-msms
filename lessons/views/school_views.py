from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from django.views.generic import FormView
from django.views.generic.edit import FormMixin

from lessons.forms import SchoolCreateForm, SchoolDeleteForm
from lessons.forms import SchoolManageForm
from lessons.models import Admission
from lessons.models import School, Lesson, User, Transfer
from lessons.views import GroupRestrictedMixin
from lessons.views.mixins import SchoolGroupRestrictedMixin
from lessons.views.mixins import SchoolObjectMixin


class HomeView(LoginRequiredMixin, ListView):
    model = School
    template_name = "school/list_school.html"
    context_object_name = "schools"

    def handle_no_permission(self):
        return redirect('index')


class TestForm(forms.Form):
    pass


class SchoolHomeView(LoginRequiredMixin, FormView):

    model = School
    template_name = "school/home.html"
    pk_url_kwarg = 'school'
    http_method_names = ['get', 'post']
    form_class = TestForm

    def get_context_data(self, **kwargs):
        context = super(SchoolHomeView, self).get_context_data(**kwargs)
        school = School.objects.get(id=self.kwargs['school'])
        context['school'] = school
        try:
            admission = Admission.objects.get(school=school, client=self.request.user)
            context['school_user_groups'] = admission.groups.all()

        except:
            admission = None
        context['in_school'] = school.has_member(self.request.user)
        context['is_not_director'] = not school.is_director(self.request.user)
        context['is_banned'] = school.get_ban(self.request.user)

        return context

    def form_valid(self, form):
        school = School.objects.get(id=self.kwargs['school'])
        if school.is_director(self.request.user):
            return super().form_valid(form)
        if form.data['follow']:
            school.set_group_client(self.request.user)
        else:
            school.leave_school(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('school_home', kwargs={'school': self.kwargs['school']})

    def handle_no_permission(self):
        return redirect('home')


class SchoolUserListView(LoginRequiredMixin, SchoolGroupRestrictedMixin, SchoolObjectMixin, ListView):
    """
    View that displays a list of users to the administrator.
    """
    model = User
    template_name = "school/users.html"
    context_object_name = "students"
    allowed_group = "Super-administrator"

    def get_queryset(self):
        school = School.objects.get(id=self.kwargs['school'])
        return User.objects.filter(Q(enrolled_school=school), ~Q(admission__groups__name='Director'))

    def handle_no_permission(self):
        return redirect('home')


class SchoolCreateView(LoginRequiredMixin, GroupRestrictedMixin, CreateView):
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

    def handle_no_permission(self):
        return redirect('home')


class SchoolSubscribeView(LoginRequiredMixin, FormView):
    model = School
    pk_url_kwarg = 'school'
    template_name = "base/school_base.html"
    form_class = SchoolManageForm
    http_method_names = ['get', 'post']

    def get_context_data(self, **kwargs):
        context = super(SchoolSubscribeView, self).get_context_data(**kwargs)
        school = School.objects.get(id=self.kwargs['school'])
        context['school'] = school
        return context

    def form_valid(self, form):
        if form.cleaned_data.get('join_school'):
            School.objects.get(id=self.kwargs['school']).set_group_client(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('manage', kwargs={'school': self.kwargs['school']})


class SchoolManageView(LoginRequiredMixin, SchoolGroupRestrictedMixin, UpdateView):
    model = School
    template_name = "school/manage_school.html"
    form_class = SchoolManageForm
    pk_url_kwarg = 'school'
    http_method_names = ['get', 'post']
    allowed_group = "Director"  # Change to director

    def form_valid(self, form):
        school = form.save()
        if form.data.get('delete_school'):
            school.delete()
            return HttpResponseRedirect(reverse('home'))
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('school_home', kwargs={'school': self.kwargs['school']})

    def handle_no_permission(self):
        return redirect('home')


class SchoolDeleteView(LoginRequiredMixin, GroupRestrictedMixin, UpdateView):
    model = School
    template_name = "school/delete_school.html"
    form_class = SchoolDeleteForm
    http_method_names = ['get', 'post']
    allowed_group = "Director"

    def form_valid(self, form):
        form.instance.director = self.request.user
        school = form.save()
        if form.data.get('delete_school'):
            school.delete()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('home')

    def handle_no_permission(self):
        return redirect('home')


