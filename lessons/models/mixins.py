from django.contrib.auth.models import Group


class GroupRegistrationMixin:
    """
    Mixin that allows a hierarchy of a group to be registered to a user.

    System Groups
    ┏━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃  System-administrator  ┃
    ┃        Director        ┃
    ┃       Adult-user       ┃
    ┃           ↓ (inherits) ┃
    ┃          User          ┃
    ┗━━━━━━━━━━━━━━━━━━━━━━━━┛
    """

    def set_group_system_administrator(self):
        system_administrator_group, created = Group.objects.get_or_create(name='System-administrator')
        self.groups.add(system_administrator_group)

    def set_group_director(self):
        director_group, created = Group.objects.get_or_create(name='Director')
        self.groups.add(director_group)

    def set_group_adult_user(self):
        adult_user_group, created = Group.objects.get_or_create(name='Adult-user')
        self.groups.add(adult_user_group)
        self.set_group_user()

    def set_group_user(self):
        user_group, created = Group.objects.get_or_create(name='User')
        self.groups.add(user_group)

    """
    Deprecated Groups (DO NOT USE)
    """

    """
    def set_group_director(self):
        director_group, created = Group.objects.get_or_create(name='Director')
        self.groups.add(director_group)
        self.set_group_super_administrator()
    """

    """
    def set_group_super_administrator(self):
        super_administrator_group, created = Group.objects.get_or_create(name='Super-administrator')
        self.groups.add(super_administrator_group)
        self.set_group_administrator()
    """

    """
    def set_group_administrator(self):
        administrator_group, created = Group.objects.get_or_create(name='Administrator')
        self.groups.add(administrator_group)
    """

    """
    def set_group_adult_student(self):
        adult_student_group, created = Group.objects.get_or_create(name='Adult-student')
        self.groups.add(adult_student_group)
        self.set_group_student()
    """

    """
    def set_group_student(self):
        student_group, created = Group.objects.get_or_create(name='Student')
        self.groups.add(student_group)
    """
