from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, ListView, UpdateView, FormView

from lessons.forms import SchoolCreateForm, SchoolManageForm
from lessons.models import School, Lesson, User, Transfer, Admission
from lessons.views import GroupRestrictedMixin
from lessons.views.mixins import SchoolObjectMixin, SchoolGroupRestrictedMixin


class HomeView(LoginRequiredMixin, ListView):
    model = School
    template_name = "school/list_school.html"
    context_object_name = "schools"

    def handle_no_permission(self):
        return redirect('index')


class SchoolHomeView(LoginRequiredMixin, SchoolGroupRestrictedMixin, SchoolObjectMixin, ListView):
    """
    View that displays the students school home page.
    """

    model = Lesson
    template_name = "school/student_home.html"
    context_object_name = "lessons"
    allowed_group = "Client"

    def get_context_data(self, **kwargs):
        context = super(SchoolHomeView, self).get_context_data(**kwargs)
        context['lessons'] = context['lessons'].filter(Q(student=self.request.user) | Q(student__parent=self.request.user)).order_by('-fulfilled')
        context['transfers'] = Transfer.objects.filter(user_id=self.request.user).filter(school=self.kwargs['school'])
        return context

    def handle_no_permission(self):
        school = School.objects.get(id=self.kwargs['school'])
        admission = Admission.objects.get(school=school, client=self.request.user)
        if admission.groups.filter(name="Administrator").exists():
            return redirect('users', school=self.kwargs['school'])
        else:
            return redirect('home')


class SchoolManageView(LoginRequiredMixin, FormView):
    model = School
    pk_url_kwarg = 'school'
    template_name = "school/manage.html"
    form_class = SchoolManageForm
    http_method_names = ['get', 'post']

    def get_context_data(self, **kwargs):
        context = super(SchoolManageView, self).get_context_data(**kwargs)
        school = School.objects.get(id=self.kwargs['school'])
        context['school'] = school
        return context

    def form_valid(self, form):
        if form.cleaned_data.get('join_school'):
            School.objects.get(id=self.kwargs['school']).set_group_client(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('manage', kwargs={'school': self.kwargs['school']})


class SchoolUserListView(LoginRequiredMixin, SchoolGroupRestrictedMixin, SchoolObjectMixin, ListView):
    """
    View that displays a list of users to the administrator.
    """
    model = User
    template_name = "school/users.html"
    context_object_name = "students"
    allowed_group = "Administrator"

    def get_context_data(self, **kwargs):
        context = super(SchoolUserListView, self).get_context_data(**kwargs)
        context['students'] = User.objects.filter(groups__name='Student').filter(lesson__school_id=self.kwargs['school'])
        return context

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
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('home')

    def handle_no_permission(self):
        return redirect('home')
