"""
Views that will be used in the music school management system.
"""

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
from lessons.models import Lesson, User, Transfer
from lessons.views.mixins import GroupRestrictedMixin, SchoolObjectMixin


class LessonRequestView(LoginRequiredMixin, GroupRestrictedMixin, SchoolObjectMixin, CreateView):
    """
    View that displays the form allowing users to request a lesson.
    If the form is valid, the user is redirected to the home page and
    a Lesson object is created.
    """

    model = Lesson
    template_name = "lessons/request_lesson.html"
    form_class = LessonRequestForm
    http_method_names = ['get', 'post']
    allowed_group = "Student"

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


class BookingListView(LoginRequiredMixin, GroupRestrictedMixin, SchoolObjectMixin, ListView):
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
        return context

    def handle_no_permission(self):
        return redirect('home')


class LessonFulfillView(LoginRequiredMixin, GroupRestrictedMixin, SchoolObjectMixin, UpdateView):
    """
    View that displays the form allowing administrators to fulfill a lesson
    request. If the form is valid, the admin is redirected to the home page
    and the corresponding Lesson object updated.
    """

    model = Lesson
    template_name = "lessons/modify_lesson.html"
    form_class = LessonFulfillForm
    http_method_names = ['get', 'post']
    allowed_group = "Administrator"

    def form_valid(self, form):
        super().form_valid(form)
        data = form.save(commit=False)
        data.price = (data.duration / 60) * data.number_of_lessons * 10
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

