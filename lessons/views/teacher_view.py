
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import ListView
from lessons.models import Lesson
from lessons.views.mixins import SchoolObjectMixin, SchoolGroupRestrictedMixin

class TimetableView(LoginRequiredMixin, SchoolGroupRestrictedMixin, SchoolObjectMixin, ListView):
    """
    View that displays all teacher lessons.
    """

    model = Lesson
    template_name = "teachers/timetable.html"
    context_object_name = "lessons"
    allowed_group = "Teacher"

    def get_context_data(self, **kwargs):
        context = super(TimetableView, self).get_context_data(**kwargs)
        context['lessons'] = context['lessons'].order_by('-fulfilled')
        return context

    def handle_no_permission(self):
        return redirect('home')