"""
Views that will be used in the music school management system.
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from lessons.models.term import Term
from lessons.helpers import administrator_restricted
from lessons.forms import TermForm

@login_required
@administrator_restricted
def view_terms(request):
    terms = Term.objects.all()

    if request.method == "POST":
        form = TermForm(request.POST)
        if form.is_valid():
            form.save()
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
