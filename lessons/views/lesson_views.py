"""
Views that will be used in the music school management system.
"""

from datetime import datetime, timedelta
from time import time
from unicodedata import name
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, ListView
from django.utils.timezone import make_aware

from lessons.forms import LessonModifyForm, LessonFulfillForm, LessonRequestForm
from lessons.helpers import lesson_fulfilled_restricted
from lessons.models import Lesson, User, School, Term, Transfer
from lessons.models.lesson import ScheduledLesson
from lessons.views.mixins import SchoolObjectMixin, SchoolGroupRestrictedMixin


class LessonListView(SchoolGroupRestrictedMixin, SchoolObjectMixin, ListView):
    """
    View that displays the students school home page.
    """

    model = Lesson
    template_name = "lessons/student_lessons.html"
    context_object_name = "lessons"
    allowed_group = "Client"

    def get_queryset(self):
        return super().get_queryset().filter(school=self.kwargs['school'])

    def get_context_data(self, **kwargs):
        context = super(LessonListView, self).get_context_data(**kwargs)
        context['lessons'] = context['lessons'].filter(
            Q(student=self.request.user) | Q(student__parent=self.request.user)).order_by('-fulfilled')
        return context


class LessonRequestView(SchoolGroupRestrictedMixin, SchoolObjectMixin, CreateView):
    """
    View that displays the form allowing users to request a lesson.
    If the form is valid, the user is redirected to the home page and
    a Lesson object is created.
    """

    model = Lesson
    template_name = "lessons/request_lesson.html"
    form_class = LessonRequestForm
    http_method_names = ['get', 'post']
    allowed_group = "Client"

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(LessonRequestView, self).get_form_kwargs(**kwargs)
        form_kwargs['school'] = self.school_instance
        form_kwargs['user'] = self.request.user
        return form_kwargs

    def form_valid(self, form):
        super().form_valid(form)
        lesson = form.save(commit=False)
        number_of_lessons = ScheduledLesson.objects.filter(
            lesson=lesson
        ).count()
        lesson.price = (lesson.duration / 60) * number_of_lessons * 10
        
        lesson.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('client_lessons', kwargs={'school': self.school_id})


class LessonModifyView(LoginRequiredMixin, SchoolObjectMixin, UpdateView):  # Required Permissions
    """
    View that displays the form allowing users to edit an existing lesson
    request. If the form is valid, the user is redirected to the home page
    and the corresponding Lesson object updated.
    """

    model = Lesson
    template_name = "lessons/modify_lesson.html"
    form_class = LessonModifyForm
    http_method_names = ['get', 'post']

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(LessonModifyView, self).get_form_kwargs(**kwargs)
        form_kwargs['school'] = self.school_instance
        form_kwargs['user'] = self.request.user
        return form_kwargs


    def form_valid(self, form):
        super().form_valid(form)
        if self.request.user == form.instance.student or self.request.user == form.instance.student.parent:
            lesson = form.save(commit=False)
            number_of_lessons = ScheduledLesson.objects.filter(
                lesson=lesson
            ).count()
            lesson.price = (lesson.duration / 60) * number_of_lessons * 10
            lesson.save()
        else:
            administrators = User.objects.filter(groups__name='Administrator')
            for admin in administrators:
                if self.request.user == admin:
                    lesson = form.save(commit=False)
                    number_of_lessons = ScheduledLesson.objects.filter(
                        lesson=lesson
                    ).count()
                    lesson.price = (lesson.duration / 60) * number_of_lessons * 10

                    lesson.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('client_lessons', kwargs={'school': self.school_id})

    def handle_no_permission(self):
        return redirect('home')


class BookingListView(SchoolGroupRestrictedMixin, SchoolObjectMixin, ListView):
    """
    View that displays all student bookings.
    """

    model = Lesson
    template_name = "lessons/bookings.html"
    context_object_name = "lessons"
    allowed_group = "Administrator"

    def get_queryset(self):
        return super().get_queryset().filter(school=self.kwargs['school'])

    def get_context_data(self, **kwargs):
        context = super(BookingListView, self).get_context_data(**kwargs)
        context['lessons'] = context['lessons'].order_by('-fulfilled')
        return context


class LessonFulfillView(SchoolGroupRestrictedMixin, SchoolObjectMixin, UpdateView):
    """
    View that displays the form allowing administrators to fulfill a lesson
    request. If the form is valid, the admin is redirected to the home page
    and the corresponding Lesson object updated.
    """

    model = Lesson
    template_name = "lessons/fulfill_lesson.html"
    form_class = LessonFulfillForm
    http_method_names = ['get', 'post']
    allowed_group = "Administrator"

    def dispatch(self, request, *args, **kwargs):
        school_instance = get_object_or_404(School, pk=self.kwargs['school'])
        self.this_term = school_instance.get_update_current_term
        if self.this_term != None and Term.objects.filter(school_id=self.kwargs['school']).count() > 1:
            self.next_term = Term.get_next_by_start_date(self.this_term, school=school_instance)
            days_to_term_end = (self.this_term.end_date - datetime.now().date()).days
            # we still have a week of term left
            if days_to_term_end >= 7:
                self.next_term = self.this_term
            # we are NOT in a term break/holiday
            if self.this_term.end_date <= datetime.now().date():
                self.next_term = self.this_term
        else:
            self.next_term = self.this_term

        return super(LessonFulfillView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        return {'start_term': self.next_term, 'school': self.kwargs['school']}

    def form_valid(self, form):
        super().form_valid(form)

        data = form.save(commit=False)

        # ensure end_date and start_date fields are always filled in
        # even if a term is selected by the user
        if data.end_date == None and self.this_term != None:
            data.end_date = self.this_term.end_date
        if data.start_type == "Term" and self.this_term != None:
            term = Term.objects.get(pk=data.start_term_id)
            data.start_date = term.start_date
        data.fulfilled = True

        self.calculateSchedule(data)

        data.number_of_lessons = ScheduledLesson.objects.filter(
            lesson=data
        ).count()
        data.price = (data.duration / 60) * data.number_of_lessons * 10
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('school_bookings', kwargs={'school': self.kwargs['school']})

    def handle_no_permission(self):
        return redirect('home')

    def calculateSchedule(self, lesson):
        duration = timedelta(minutes=lesson.duration)
        interval = timedelta(weeks=lesson.interval)
        date = lesson.start_date
        
        while date.strftime('%A') != lesson.day:
            date += timedelta(days=1)

        current = datetime.combine(date, lesson.time)
        
        while current.date() <= lesson.end_date:
            sl = ScheduledLesson.objects.create(
                lesson = Lesson.objects.get(pk=lesson.id),
                start = make_aware(current),
                end = make_aware(current + duration),
            )

            current += interval


@method_decorator(lesson_fulfilled_restricted, name='dispatch')
class LessonInvoiceView(LoginRequiredMixin, SchoolObjectMixin, ListView):
    """
    View that displays to the User details of a booking after it has been confirmed by and Admin
    """

    model = Lesson
    template_name = "lessons/invoice.html"
    context_object_name = "lessons"

    def get_queryset(self):
        return super().get_queryset().filter(school=self.kwargs['school'])

    def get_context_data(self, **kwargs):
        context = super(LessonInvoiceView, self).get_context_data(**kwargs)
        context['lessons'] = Lesson.objects.filter(id=self.kwargs['pk'])
        context['transfers'] = Transfer.objects.filter(lesson=self.kwargs['pk'])
        return context
