"""
Views that will be used in the music school management system.
"""

from webbrowser import get
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView, UpdateView

from lessons.models import Term, School
from lessons.helpers import administrator_restricted
from lessons.forms import TermForm, LessonModifyForm, term_forms
from lessons.models import School, Term, Lesson, User
from lessons.views.mixins import GroupRestrictedMixin, SchoolObjectMixin


class TermsView(LoginRequiredMixin, GroupRestrictedMixin, SchoolObjectMixin, CreateView):
    model = Term
    template_name = "terms/terms.html"
    form_class = TermForm
    http_method_names = ['get', 'post']
    allowed_group = "Administrator"

    def form_valid(self, form):
        super().form_valid(form)
        term = form.save()
        if Term.objects.count() == 1:
            school_instance = School.objects.get(name="KCL Kangaroos")
            setattr(school_instance, 'current_term', term)
            school_instance.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        kwargs['terms'] = Term.objects.all()
        return super(TermsView, self).get_context_data(**kwargs)

    def get_success_url(self):
        return reverse('terms', kwargs={'school': self.kwargs['school']})

    def handle_no_permission(self):
        return redirect('home')

class TermEditView(LoginRequiredMixin, GroupRestrictedMixin, SchoolObjectMixin, UpdateView):
    model = Term
    template_name = "terms/edit_term.html"
    form_class = TermForm
    http_method_names = ['get', 'post']
    allowed_group = "Administrator"

    # def dispatch(self, request, *args, **kwargs):
    #     data = get_object_or_404(Term, id=self.kwargs['pk'])
    #     print(data)
    #     try:
    #         term = Term.objects.get(pk=self.kwargs['pk'])
    #         print(term)
    #     except Term.DoesNotExist:
    #         term = None
    #         print("DOESN'T EXIST")

    #     return super().dispatch(request, *args, **kwargs)

    # def get_context_data(self, **kwargs):
    #     context = super(TermEditView, self).get_context_data(**kwargs)
    #     context['school'] = School.objects.filter(id=self.kwargs['school'])[0]
    #     return context

    def form_valid(self, form):
        #form.instance.term_id = self.kwargs['pk']
        super().form_valid(form)
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('terms', kwargs={'school': self.kwargs['school']})

    def handle_no_permission(self):
        return redirect('home')
