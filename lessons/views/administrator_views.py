"""
Views that will be used in the music school management system.
"""
from django.db.models import Q
from django.urls import reverse
from django.views.generic import ListView, FormView, UpdateView

from lessons.forms import ManageMemberForm
from lessons.models import User, School, Admission
from lessons.views.mixins import SchoolObjectMixin, SchoolGroupRestrictedMixin


class ManageStudentView(SchoolGroupRestrictedMixin, FormView):  # SchoolObjectMixin
    """
    View that displays the manage student page and forms. Allowing for the 
    promotion of users. If a valid form is submitted the user is redirected to the members page.
    """

    template_name = "authentication/manage_student.html"
    form_class = ManageMemberForm
    http_method_names = ['get', 'post']
    allowed_group = "Director"

    def dispatch(self, *args, **kwargs):
        school = School.objects.get(id=self.kwargs['school'])
        if self.kwargs['pk'] == school.director_id:
            return self.handle_no_permission()
        return super().dispatch(*args, **kwargs)

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
    context_object_name = "school_admissions"
    allowed_group = "Super-administrator"

    def get_queryset(self):
        first_name_query = self.request.GET.get('search_first_name', "")
        last_name_query = self.request.GET.get('search_last_name', "")
        context = Admission.objects.filter(Q(school=self.school_instance),
                                           Q(client__first_name__contains=first_name_query),
                                           Q(client__last_name__contains=last_name_query),
                                           ~Q(school=self.school_instance, groups__name='Director'))
        return context


    def get_context_data(self, **kwargs):
        context = super(SchoolUserListView, self).get_context_data(**kwargs)
        context['search_first_name'] = self.request.GET.get('search_first_name', "")
        context['search_last_name'] = self.request.GET.get('search_last_name', "")
        return context
