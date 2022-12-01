from django.contrib.auth.models import Group


class GroupRegistrationMixin:
    """
    Mixin that allows a hierarchy of a group to be registered to a user.
    """

    def set_group_director(self):
        director_group, created = Group.objects.get_or_create(name='Director')
        self.groups.add(director_group)
        self.set_group_super_administrator()

    def set_group_super_administrator(self):
        super_administrator_group, created = Group.objects.get_or_create(name='Super-administrator')
        self.groups.add(super_administrator_group)
        self.set_group_administrator()

    def set_group_administrator(self):
        administrator_group, created = Group.objects.get_or_create(name='Administrator')
        self.groups.add(administrator_group)

    def set_group_adult_student(self):
        adult_student_group, created = Group.objects.get_or_create(name='Adult-student')
        self.groups.add(adult_student_group)
        self.set_group_student()

    def set_group_student(self):
        student_group, created = Group.objects.get_or_create(name='Student')
        self.groups.add(student_group)


class GroupRestrictedMixin:
    """
    Mixin that only allows a specified group to access a view to users that are logged in.
    """

    allowed_group = None

    def dispatch(self, *args, **kwargs):
        if not self.request.user.groups.filter(name=self.allowed_group).exists():
            return self.handle_no_permission()
        return super().dispatch(*args, **kwargs)
