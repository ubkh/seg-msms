"""
Views that will be used in the music school management system.
"""

from ast import And, Not
from datetime import datetime
from unicodedata import name
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from lessons.forms import LessonModifyForm, LessonFulfillForm, LessonRequestForm
from lessons.models import Lesson, User, Transfer, School, Term
from lessons.views import home
from lessons.helpers import administrator_restricted, lesson_fulfilled_restricted


@login_required
def request_lesson(request):
    """
    View that displays the form allowing users to request a lesson.
    If the form is valid, the user is redirected to the home page and 
    a Lesson object is created.
    """
    if request.method == "POST":
        form = LessonRequestForm(request.POST, user=request.user)
        if form.is_valid():
            # form.instance.student = request.user
            lesson = form.save(commit=False)
            lesson.price = (lesson.duration/60)*lesson.number_of_lessons*10
            lesson.save()
            return redirect('home')
    else:
        form = LessonRequestForm(user=request.user)
    return render(request, "lessons/request_lesson.html", {'form': form})


@login_required
def modify_lesson(request, pk):
    """
    View that displays the form allowing users to edit an existing lesson
    request. If the form is valid, the user is redirected to the home page
    and the corresponding Lesson object updated.
    """
    data = get_object_or_404(Lesson, id=pk)
    form = LessonModifyForm(instance=data)

    if request.method == "POST":
        form = LessonModifyForm(request.POST, instance=data)

        if form.is_valid():
            if request.user == form.instance.student or request.user == form.instance.student.parent:
                # form.instance.student = request.user
                lesson = form.save(commit=False)
                lesson.price = (lesson.duration/60)*lesson.number_of_lessons*10
                lesson.save()
                return redirect('home')
            else:
                administrators = User.objects.filter(groups__name='Administrator')
                for admin in administrators:
                    if request.user == admin:
                        lesson = form.save(commit=False)
                        lesson.price = (lesson.duration/60)*lesson.number_of_lessons*10
                        lesson.save()
                        return redirect('home')
    return render(request, "lessons/modify_lesson.html", {'form': form})


@login_required
@administrator_restricted
def open_bookings(request, pk):
    """
    View that displays all student bookings.
    """
    s = get_object_or_404(User, id=pk)
    current_student = User.objects.filter(id=pk)
    lessons = Lesson.objects.filter(student=s).order_by('-fulfilled')
    transfers = Transfer.objects.filter(user=s)
    return render(request, "lessons/bookings.html",
                  {'current_student': current_student, 'lessons': lessons, 'transfers': transfers})


@login_required
@administrator_restricted
def fulfill_lesson(request, pk):
    """
    View that displays the form allowing administrators to fulfill a lesson
    request. If the form is valid, the admin is redirected to the home page
    and the corresponding Lesson object updated.
    """
    
    school_instance = School.objects.get(name="KCL Kangaroos")
    #this_term = school_instance.current_term
    this_term = school_instance.get_update_current_term
    print(this_term)
    if this_term != None and Term.objects.count() > 1:
        next_term = Term.get_next_by_start_date(this_term)
        days_to_term_end = (this_term.end_date - datetime.now().date()).days
        # we still have a week of term left
        if days_to_term_end >= 7:
            next_term = this_term
        # we are NOT in a term break/holiday
        if this_term.end_date <= datetime.now().date():
            next_term = this_term
    else:
        next_term = this_term

    data = get_object_or_404(Lesson, id=pk)
    form = LessonFulfillForm(instance=data, initial={'start_term': next_term})

    if request.method == "POST":
        form = LessonFulfillForm(request.POST, instance=data)

        if form.is_valid():
            data.price = (data.duration/60) * data.number_of_lessons * 10
            if data.end_date == None and this_term != None:
                data.end_date = this_term.end_date
            lesson = form.save(commit=False)
            lesson.fulfilled = True
            lesson.save()
            return redirect(home)
    return render(request, "lessons/fulfill_lesson.html", {'form': form})

@login_required
@lesson_fulfilled_restricted
def booking_invoice(request, pk):
    """
    View that displays to the User details of a booking after it has been confirmed by and Admin
    """
    lessons = Lesson.objects.filter(id=pk)
    return render(request, "lessons/invoice.html", {'lessons': lessons})

