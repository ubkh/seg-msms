from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, ListView, UpdateView

from lessons.forms import SchoolCreateForm, SchoolDeleteForm
from lessons.models import School, Lesson, User, Transfer
from lessons.views import GroupRestrictedMixin
from lessons.views.mixins import SchoolObjectMixin
from django.http import HttpResponseRedirect

class HomeView(LoginRequiredMixin, ListView):
    model = School
    template_name = "school/list_school.html"
    context_object_name = "schools"

    def handle_no_permission(self):
        return redirect('index')


class SchoolHomeView(LoginRequiredMixin, GroupRestrictedMixin, SchoolObjectMixin, ListView):
    """
    View that displays the students school home page.
    """

    model = Lesson
    template_name = "school/student_home.html"
    context_object_name = "lessons"
    allowed_group = "Student"

    def get_context_data(self, **kwargs):
        context = super(SchoolHomeView, self).get_context_data(**kwargs)
        context['lessons'] = context['lessons'].filter(Q(student=self.request.user) | Q(student__parent=self.request.user)).order_by('-fulfilled')
        context['transfers'] = Transfer.objects.filter(user_id=self.request.user).filter(school=self.kwargs['school'])
        return context

    def handle_no_permission(self):
        if self.request.user.groups.filter(name='Administrator').exists():
            return redirect('users', school=self.kwargs['school'])
        else:
            return redirect('home')


class SchoolUserListView(LoginRequiredMixin, GroupRestrictedMixin, SchoolObjectMixin, ListView):
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

