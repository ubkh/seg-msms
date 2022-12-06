from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect

from lessons.models import School, Admission


class GroupRestrictedMixin(LoginRequiredMixin):
    """
    Mixin that only allows a specified group to access a view to users that are logged in.
    """

    allowed_group = None

    def dispatch(self, *args, **kwargs):
        if not self.request.user.groups.filter(name=self.allowed_group).exists():
            return self.handle_no_permission()
        return super().dispatch(*args, **kwargs)


class SchoolGroupRestrictedMixin(LoginRequiredMixin):
    allowed_group = None

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_anonymous:
            return self.handle_no_permission()
        school = School.objects.get(id=self.kwargs['school'])
        try:
            admission = Admission.objects.get(school=school, client=self.request.user)
        except Admission.DoesNotExist:
            admission = None
        if not admission or not admission.is_active or not admission.groups.filter(name=self.allowed_group).exists():
            return self.handle_no_permission()
        return super().dispatch(*args, **kwargs)

    def handle_no_permission(self):
        return redirect('home')


class SchoolObjectMixin:

    def dispatch(self, request, *args, **kwargs):
        self.school_id = self.kwargs['school']
        self.school_instance = get_object_or_404(School, id=self.school_id)
        try:
            admission = Admission.objects.get(school=self.school_instance, client=self.request.user)
            self.admission_groups = admission.groups.all()
        except Admission.DoesNotExist:
            self.admission_groups = None
        return super(SchoolObjectMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SchoolObjectMixin, self).get_context_data(**kwargs)
        context['school'] = self.school_instance
        context['school_user_groups'] = self.admission_groups
        context['in_school'] = self.school_instance.has_member(self.request.user)
        context['is_not_director'] = not self.school_instance.is_director(self.request.user)
        context['is_banned'] = self.school_instance.get_ban(self.request.user)
        return context

    def form_valid(self, form):
        form.instance.school_id = self.school_id
        return super().form_valid(form)
