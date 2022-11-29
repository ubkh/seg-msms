"""
Views that will be used in the music school management system.
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from lessons.models.term import Term
from lessons.helpers import administrator_restricted

@login_required
@administrator_restricted
def view_terms(request):
    terms = Term.objects.all()
    return render(request, "terms/terms.html", {'terms': terms})
