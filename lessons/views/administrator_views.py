"""
Views that will be used in the music school management system.
"""

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, FormView

from lessons.forms import RegisterForm, AdminModifyForm, BanClientForm, ManageMemberForm
from lessons.helpers import super_administrator_restricted
from lessons.models import User, School, Admission
from lessons.views.mixins import GroupRestrictedMixin, SchoolObjectMixin, SchoolGroupRestrictedMixin


class ManageStudentView(LoginRequiredMixin, SchoolGroupRestrictedMixin, FormView):

    template_name = "authentication/manage_student.html"
    form_class = ManageMemberForm
    http_method_names = ['get', 'post']
    allowed_group = "Director"

    def get_context_data(self, **kwargs):
        context = super(ManageStudentView, self).get_context_data(**kwargs)
        school = School.objects.get(id=self.kwargs['school'])
        context['school'] = school
        admission = Admission.objects.get(school=school, client=self.request.user)
        context['school_user_groups'] = admission.groups.all()
        return context

    def get_initial(self):
        initial = super().get_initial()
        school = School.objects.get(id=self.kwargs['school'])
        initial['client'] = school.is_client(self.kwargs['pk'])
        initial['teacher'] = school.is_teacher(self.kwargs['pk'])
        initial['administrator'] = school.is_administrator(self.kwargs['pk'])
        initial['super_administrator'] = school.is_super_administrator(self.kwargs['pk'])
        initial['ban_member'] = school.get_ban(self.kwargs['pk'])
        return initial

    def form_valid(self, form):
        school = School.objects.get(id=self.kwargs['school'])
        school.leave_school(self.kwargs['pk'])

        if form.cleaned_data.get('client'):
            school.set_group_administrator(self.kwargs['pk'])

        if form.cleaned_data.get('teacher'):
            school.set_group_teacher(self.kwargs['pk'])

        if form.cleaned_data.get('administrator'):
            school.set_group_administrator(self.kwargs['pk'])

        if form.cleaned_data.get('super_administrator'):
            school.set_group_super_administrator(self.kwargs['pk'])

        if form.cleaned_data.get('ban_member'):
            school.ban_member(self.kwargs['pk'])
        else:
            school.unban_member(self.kwargs['pk'])

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('members', kwargs={'school': self.kwargs['school']})

    def handle_no_permission(self):
        return redirect('home')


class BanClientView(LoginRequiredMixin, SchoolGroupRestrictedMixin, UpdateView):

    model = User
    template_name = "authentication/ban_client.html"
    form_class = BanClientForm
    http_method_names = ['get', 'post']
    allowed_group = "Super-administrator" # Change to director

    def get_success_url(self):
        return reverse('members', kwargs={'school': self.kwargs['school']})

    def handle_no_permission(self):
        return redirect('home')


