from lessons.models import School, Admission


class GroupRestrictedMixin:
    """
    Mixin that only allows a specified group to access a view to users that are logged in.
    """

    allowed_group = None

    def dispatch(self, *args, **kwargs):
        if not self.request.user.groups.filter(name=self.allowed_group).exists():
            return self.handle_no_permission()
        return super().dispatch(*args, **kwargs)


class SchoolGroupRestrictedMixin:
    allowed_group = None

    def dispatch(self, *args, **kwargs):
        school = School.objects.get(id=self.kwargs['school'])
        try:
            admission = Admission.objects.get(school=school, client=self.request.user)
        except Admission.DoesNotExist:
            admission = None
        if not admission or not admission.is_active or not admission.groups.filter(name=self.allowed_group).exists():
            return self.handle_no_permission()
        return super().dispatch(*args, **kwargs)


class SchoolObjectMixin:

    def get_context_data(self, **kwargs):
        context = super(SchoolObjectMixin, self).get_context_data(**kwargs)
        school = School.objects.get(id=self.kwargs['school'])
        context['school'] = school
        admission = Admission.objects.get(school=school, client=self.request.user)
        context['school_user_groups'] = admission.groups.all()
        return context

    # Remove vvvvv
    def get_queryset(self):
        return super().get_queryset().filter(school=self.kwargs['school'])

    def form_valid(self, form):
        form.instance.school_id = self.kwargs['school']
        return super().form_valid(form)
