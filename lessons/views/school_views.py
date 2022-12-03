from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, ListView

from lessons.forms import SchoolCreateForm
from lessons.models import School, Lesson, User, Transfer
from lessons.views import GroupRestrictedMixin
from lessons.views.mixins import SchoolObjectMixin


class SchoolHomeView(LoginRequiredMixin, SchoolObjectMixin, ListView):
    """
    View that displays the user's home page.
    """
    model = Lesson
    template_name = "school/school_home.html"

    def get_context_data(self, **kwargs):
        context = super(SchoolHomeView, self).get_context_data(**kwargs)
        context['student'] = User.objects.filter(groups__name='Student')
        context['lessons'] = Lesson.objects.filter(Q(student=self.request.user) | Q(student__parent=self.request.user)).order_by('-fulfilled') # (Q(id=self.user.id) | Q(parent=self.user))
        context['administrators'] = User.objects.filter(groups__name='Administrator')
        context['transfers'] = Transfer.objects.filter(user_id=self.request.user)
        return context

    def handle_no_permission(self):
        return redirect('home')


class SchoolListView(LoginRequiredMixin, ListView):  # GroupRestrictedMixin
    model = School
    template_name = "school/list_school.html"
    context_object_name = "schools"
    allowed_group = "Student"

    def handle_no_permission(self):
        return redirect('home')


class SchoolCreateView(LoginRequiredMixin, CreateView):  # GroupRestrictedMixin
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
