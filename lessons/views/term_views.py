"""
Views that will be used in the music school management system.
"""

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, UpdateView

from lessons.forms import TermForm
from lessons.models import School, Term
from lessons.views.mixins import SchoolObjectMixin, SchoolGroupRestrictedMixin


class TermsView(SchoolGroupRestrictedMixin, SchoolObjectMixin, CreateView):
    """
    View that displays the term page and term forms. If a valid 
    form is submitted the user is redirected to the term page.
    """

    model = Term
    template_name = "terms/terms.html"
    form_class = TermForm
    http_method_names = ['get', 'post']
    allowed_group = "Administrator"

    def form_valid(self, form):
        super().form_valid(form)
        term = form.save()
        if Term.objects.filter(school_id=self.kwargs['school']).count() == 1:
            school_instance = get_object_or_404(School, pk=self.kwargs['school'])
            setattr(school_instance, 'current_term', term)
            school_instance.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_initial(self):
        return {'school': self.kwargs['school']}

    def get_context_data(self, **kwargs):
        kwargs['terms'] = Term.objects.filter(school_id=self.kwargs['school'])
        return super(TermsView, self).get_context_data(**kwargs)

    def get_success_url(self):
        return reverse('terms', kwargs={'school': self.school_id})


class TermEditView(SchoolGroupRestrictedMixin, SchoolObjectMixin, UpdateView):
    """
    View that displays the edit term page and edit term forms. If a valid 
    form is submitted the user is redirected to the term page.
    """

    model = Term
    template_name = "terms/edit_term.html"
    form_class = TermForm
    http_method_names = ['get', 'post']
    allowed_group = "Administrator"

    def form_valid(self, form):
        super().form_valid(form)
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_initial(self):
        return {'school': self.kwargs['school']}

    def get_success_url(self):
        return reverse('terms', kwargs={'school': self.school_id})
