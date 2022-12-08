from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import ListView
from django.db.models import Q

from lessons.models.lesson import ScheduledLesson
from lessons.models import School, User
from lessons.views.mixins import SchoolObjectMixin, SchoolGroupRestrictedMixin

class TimetableView(SchoolGroupRestrictedMixin, SchoolObjectMixin, ListView):
    """
    View that displays all lessons that have been scheduled for the current term.
    """

    model = ScheduledLesson
    template_name = "timetable/timetable.html"
    context_object_name = "schedule"
    allowed_group = "Client"

    def get_queryset(self):
        school = School.objects.get(pk=self.kwargs['school'])
        term = school.get_update_current_term
        if term:
            # get all scheduled lessons that follow these constraints
            parent = ScheduledLesson.objects.filter(
                Q(lesson__school=school.id),
                Q(lesson__student=self.request.user),
                (Q(lesson__start_date__gte=school.get_update_current_term.start_date)
                & Q(lesson__start_date__lte=school.get_update_current_term.end_date))
                | (Q(lesson__end_date__gte=school.get_update_current_term.start_date)
                & Q(lesson__end_date__lte=school.get_update_current_term.end_date))
            ).order_by('start')
            children = User.objects.filter(parent=self.request.user)
            for child in children:

                children = ScheduledLesson.objects.filter(
                    Q(lesson__school=school.id),
                    Q(lesson__student=child),
                    (Q(lesson__start_date__gte=school.get_update_current_term.start_date)
                    & Q(lesson__start_date__lte=school.get_update_current_term.end_date))
                    | (Q(lesson__end_date__gte=school.get_update_current_term.start_date)
                    & Q(lesson__end_date__lte=school.get_update_current_term.end_date))
                ).order_by('start')
                parent = parent | children

            return parent

        return ScheduledLesson.objects.filter(
                Q(lesson__school=school.id),
                Q(lesson__student=self.request.user),
                
        ).order_by('start')

    def handle_no_permission(self):
        return redirect('home')


class ChildrenTimetableView(SchoolGroupRestrictedMixin, SchoolObjectMixin, ListView):
    """
    View that displays all lessons that have been scheduled for the current term.
    """

    model = ScheduledLesson
    template_name = "timetable/timetable.html"
    context_object_name = "schedule"
    allowed_group = "Client"

    def get_queryset(self):
        school = School.objects.get(pk=self.kwargs['school'])
        term = school.get_update_current_term
        if term:
            # get all scheduled lessons that follow these constraints
            return ScheduledLesson.objects.filter(
                Q(lesson__school=school.id),
                Q(lesson__student=User.objects.filter(parent=self.request.user)),
                (Q(lesson__start_date__gte=school.get_update_current_term.start_date)
                & Q(lesson__start_date__lte=school.get_update_current_term.end_date))
                | (Q(lesson__end_date__gte=school.get_update_current_term.start_date)
                & Q(lesson__end_date__lte=school.get_update_current_term.end_date))
            ).order_by('start')

        return ScheduledLesson.objects.filter(
                Q(lesson__school=school.id),
                Q(lesson__student=self.request.user),
                
        ).order_by('start')

    def handle_no_permission(self):
        return redirect('home')