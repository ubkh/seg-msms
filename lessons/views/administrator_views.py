"""
Views that will be used in the music school management system.
"""
from django.db.models import Q
from django.urls import reverse
from django.views.generic import ListView, FormView

from lessons.forms import ManageMemberForm
from lessons.models import User, School, Admission
from lessons.views.mixins import SchoolObjectMixin, SchoolGroupRestrictedMixin


class ManageStudentView(SchoolGroupRestrictedMixin, FormView): # SchoolObjectMixin
    template_name = "authentication/manage_student.html"
    form_class = ManageMemberForm
    http_method_names = ['get', 'post']
    allowed_group = "Director"

    def form_valid(self, **kwargs):
        pass

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
            school.set_group_client(self.kwargs['pk'])

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
        return reverse('members', kwargs={'school': self.kwargs['school']})  # self.school_id


class SchoolUserListView(SchoolGroupRestrictedMixin, SchoolObjectMixin, ListView):
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
