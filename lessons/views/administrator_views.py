"""
Views that will be used in the music school management system.
"""

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, FormView

from lessons.forms import RegisterForm, AdminModifyForm, BanClientForm, MakeAdministratorForm
from lessons.helpers import super_administrator_restricted
from lessons.models import User, School, Admission
from lessons.views.mixins import GroupRestrictedMixin, SchoolObjectMixin, SchoolGroupRestrictedMixin


class AdministratorListView(LoginRequiredMixin, SchoolGroupRestrictedMixin, SchoolObjectMixin, ListView):
    """

    """

    model = User
    template_name = "administrators/administrators.html"
    context_object_name = "administrators"
    allowed_group = "Super-administrator"

    def get_queryset(self):
        school = School.objects.get(id=self.kwargs['school'])
        return User.objects.filter(enrolled_school=school, admission__groups__name='Administrator')

    def handle_no_permission(self):
        return redirect('home')


class AdministratorCreateView(LoginRequiredMixin, SchoolGroupRestrictedMixin, SchoolObjectMixin, CreateView):
    """
    View that displays the form to register an administrator. If a valid
    form is submitted the director is redirected to the home page, else they are
    directed to resubmit the form again.
    """

    model = User
    template_name = "authentication/register.html"
    form_class = RegisterForm
    http_method_names = ['get', 'post']
    allowed_group = "Super-administrator"

    def form_valid(self, form):
        administrator = form.save()
        school = School.objects.get(id=self.kwargs['school'])
        school.set_group_administrator(administrator)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('administrators', kwargs={'school': self.kwargs['school']})

    def handle_no_permission(self):
        return redirect('home')


class AdministratorUpdateView(LoginRequiredMixin, SchoolGroupRestrictedMixin, UpdateView):
    """
    View that displays the form to edit an administrator. If a valid
    form is submitted the director is redirected to the home page, else they are
    directed to resubmit the form again.
    """
    model = User
    template_name = "authentication/register.html"
    form_class = AdminModifyForm
    http_method_names = ['get', 'post']
    allowed_group = "Super-administrator"

    def form_valid(self, form):
        user = form.save()
        if form.data.get('make_account_super_administrator'):
            user.groups.clear()
            user.set_group_super_administrator()
        if form.data.get('delete_account'):
            user.delete()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('administrators', kwargs={'school': self.kwargs['school']})

    def handle_no_permission(self):
        return redirect('home')


class ManageStudentView(LoginRequiredMixin, SchoolGroupRestrictedMixin, FormView):

    model = User
    template_name = "authentication/manage_student.html"
    form_class = MakeAdministratorForm
    http_method_names = ['get', 'post']
    allowed_group = "Super-administrator"

    def get_context_data(self, **kwargs):
        context = super(ManageStudentView, self).get_context_data(**kwargs)
        school = School.objects.get(id=self.kwargs['school'])
        context['school'] = school
        admission = Admission.objects.get(school=school, client=self.request.user)
        context['school_user_groups'] = admission.groups.all()
        return context


    def form_valid(self, form):
        if form.cleaned_data.get('make_administrator'):
            School.objects.get(id=self.kwargs['school']).set_group_administrator(self.kwargs['pk'])
        if form.cleaned_data.get('make_super_administrator'):
            School.objects.get(id=self.kwargs['school']).set_group_super_administrator(self.kwargs['pk'])
        if form.cleaned_data.get('make_teacher'):
            School.objects.get(id=self.kwargs['school']).set_group_teacher(self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('school_home', kwargs={'school': self.kwargs['school']})

    def handle_no_permission(self):
        return redirect('home')


class BanClientView(LoginRequiredMixin, SchoolGroupRestrictedMixin, UpdateView):

    model = User
    template_name = "authentication/ban_client.html"
    form_class = BanClientForm
    http_method_names = ['get', 'post']
    allowed_group = "Super-administrator" # Change to director

    def get_success_url(self):
        return reverse('school_home', kwargs={'school': self.kwargs['school']})

    def handle_no_permission(self):
        return redirect('home')



# @login_required
# @super_administrator_restricted
# def ban_client(request, pk):
#     """"
#     View used to ban clients
#     """
#     user = get_object_or_404(User, id=pk)
#     form = BanClientForm(instance=user)

#     if request.method == "POST":
#         form = BanClientForm(request.POST, instance=user)
#         if form.is_valid():
#             form.save()
#             return redirect('home')

#     return render(request, "authentication/ban_client.html", {'form': form})
