"""
Views that will be used in the music school management system.
"""

from ast import And, Not
from datetime import datetime
from unicodedata import name
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, ListView

from lessons.forms import LessonModifyForm, LessonFulfillForm, LessonRequestForm
from lessons.helpers import administrator_restricted, lesson_fulfilled_restricted
from lessons.models import Lesson, User, Transfer, School, Term
from lessons.views.mixins import GroupRestrictedMixin, SchoolObjectMixin, SchoolGroupRestrictedMixin


class LessonRequestView(LoginRequiredMixin, SchoolGroupRestrictedMixin, SchoolObjectMixin, CreateView):
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
        form_kwargs['user'] = self.request.user
        return form_kwargs

    def form_valid(self, form):
        super().form_valid(form)
        lesson = form.save(commit=False)
        lesson.price = (lesson.duration / 60) * lesson.number_of_lessons * 10
        lesson.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('school_home', kwargs={'school': self.kwargs['school']})

    def handle_no_permission(self):
        return redirect('home')


class LessonModifyView(LoginRequiredMixin, SchoolObjectMixin, UpdateView):
    """
    View that displays the form allowing users to edit an existing lesson
    request. If the form is valid, the user is redirected to the home page
    and the corresponding Lesson object updated.
    """

    model = Lesson
    template_name = "lessons/modify_lesson.html"
    form_class = LessonModifyForm
    http_method_names = ['get', 'post']

    def form_valid(self, form):
        super().form_valid(form)
        if self.request.user == form.instance.student or self.request.user == form.instance.student.parent:
            lesson = form.save(commit=False)
            lesson.price = (lesson.duration / 60) * lesson.number_of_lessons * 10
            lesson.save()
        else:
            administrators = User.objects.filter(groups__name='Administrator')
            for admin in administrators:
                if self.request.user == admin:
                    lesson = form.save(commit=False)
                    lesson.price = (lesson.duration / 60) * lesson.number_of_lessons * 10
                    lesson.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('school_home', kwargs={'school': self.kwargs['school']})

    def handle_no_permission(self):
        return redirect('home')


class BookingListView(LoginRequiredMixin, SchoolGroupRestrictedMixin, SchoolObjectMixin, ListView):
    """
    View that displays all student bookings.
    """

    model = Lesson
    template_name = "lessons/bookings.html"
    context_object_name = "lessons"
    allowed_group = "Administrator"


    def get_context_data(self, **kwargs):
        context = super(BookingListView, self).get_context_data(**kwargs)
        s = get_object_or_404(User, id=self.kwargs['pk'])
        context['lessons'] = context['lessons'].filter(student=s).order_by('-fulfilled')
        context['transfers'] = Transfer.objects.filter(user=s).filter(school=self.kwargs['school'])
        context['student'] = s
        return context

    def handle_no_permission(self):
        return redirect('home')


class LessonFulfillView(LoginRequiredMixin, SchoolGroupRestrictedMixin, SchoolObjectMixin, UpdateView):
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
        print(self.kwargs)

        school_instance = School.objects.get(name="KCL Kangaroos")
        self.this_term = school_instance.get_update_current_term
        if self.this_term != None and Term.objects.count() > 1:
            self.next_term = Term.get_next_by_start_date(self.this_term)
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
        return {'start_term': self.next_term}

    def form_valid(self, form):
        super().form_valid(form)


        data = form.save(commit=False)
        data.price = (data.duration / 60) * data.number_of_lessons * 10
        if data.end_date == None and self.this_term != None:
            data.end_date = self.this_term.end_date
        data.fulfilled = True
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('school_home', kwargs={'school': self.kwargs['school']})

    def handle_no_permission(self):
        return redirect('home')


@method_decorator(lesson_fulfilled_restricted, name='dispatch')
class BookingInvoiceView(LoginRequiredMixin, SchoolObjectMixin, ListView):
    """
    View that displays to the User details of a booking after it has been confirmed by and Admin
    """

    model = Lesson
    template_name = "lessons/invoice.html"
    context_object_name = "lessons"

    def get_context_data(self, **kwargs):
        context = super(BookingInvoiceView, self).get_context_data(**kwargs)
        context['lessons'] = Lesson.objects.filter(id=self.kwargs['pk'])
        return context

