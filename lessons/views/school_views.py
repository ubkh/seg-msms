from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, ListView

from lessons.forms import SchoolCreateForm
from lessons.mixins import GroupRestrictedMixin
from lessons.models import School

class SchoolListView(LoginRequiredMixin, GroupRestrictedMixin, ListView):
    model = School
    template_name = "school/list_school.html"
    context_object_name = "schools"
    allowed_group = "Student"

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
