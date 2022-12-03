from lessons.models import School


class GroupRestrictedMixin:
    """
    Mixin that only allows a specified group to access a view to users that are logged in.
    """

    allowed_group = None

    def dispatch(self, *args, **kwargs):
        if not self.request.user.groups.filter(name=self.allowed_group).exists():
            return self.handle_no_permission()
        return super().dispatch(*args, **kwargs)


class SchoolObjectMixin:

    def get_context_data(self, **kwargs):
        context = super(SchoolObjectMixin, self).get_context_data(**kwargs)
        school = School.objects.get(id=self.kwargs['school'])
        context['school'] = school
        return context

    def get_queryset(self):
        return super().get_queryset().filter(school=self.kwargs['school'])

    def form_valid(self, form):
        form.instance.school_id = self.kwargs['school']
        return super().form_valid(form)