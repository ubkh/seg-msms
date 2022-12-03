"""
Views that will be used in the music school management system.
"""

import re
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from lessons.models import Term, School
from lessons.helpers import administrator_restricted
from lessons.forms import TermForm

@login_required
@administrator_restricted
def view_terms(request):
    terms = Term.objects.all()

    if request.method == "POST":
        form = TermForm(request.POST)
        if form.is_valid():
            term = form.save()

            if Term.objects.count() == 1:
                school_instance = School.objects.get(name="KCL Kangaroos")
                setattr(school_instance, 'current_term', term)
                school_instance.save()
            return redirect('terms')
    else:
        form = TermForm()
    return render(request, "terms/terms.html", {'terms': terms, 'form': form})

@login_required
@administrator_restricted
def edit_term(request, pk):
    data = get_object_or_404(Term, id=pk)

    if request.method == "POST":
        form = TermForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('terms')
    else:
        form = TermForm(instance=data)
    return render(request, "terms/edit_term.html", {'form': form})
