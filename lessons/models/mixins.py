from django.contrib.auth.models import Group
from django.apps import apps


class GroupRegistrationMixin:
    """
    Mixin that allows a hierarchy of a group to be registered to a user.

    System Groups
    ┏━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃  System-administrator  ┃
    ┃        Director        ┃
    ┃           ↓ (inherits) ┃
    ┃       Adult-user       ┃
    ┃           ↓ (inherits) ┃
    ┃          User          ┃
    ┗━━━━━━━━━━━━━━━━━━━━━━━━┛
    """

    def _set_group(self, group):
        group, created = Group.objects.get_or_create(name=group)
        self.groups.add(group)

    def set_group_system_administrator(self):
        self._set_group('System-administrator')

    def set_group_director(self):
        self._set_group('Director')
        self.set_group_adult_user()

    def set_group_adult_user(self):
        self._set_group('Adult-user')
        self.set_group_user()

    def set_group_user(self):
        self._set_group('User')


class AdmissionMixin:
    """
    Mixin that allows a school to add a group to a specified user.

    School Groups
    ┏━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃        Director        ┃
    ┃           ↓ (inherits) ┃
    ┃   Super-administrator  ┃
    ┃           ↓ (inherits) ┃
    ┃     Administrator      ┃
    ┃         Teacher        ┃
    ┃         Client         ┃
    ┗━━━━━━━━━━━━━━━━━━━━━━━━┛
    """

    def _get_user_admission(self, user):
        user_admission, created = apps.get_model('lessons.Admission').objects.get_or_create(school=self, client=user)
        return user_admission

    def leave_school(self, user):
        user_admission = self._get_user_admission(user)
        user_admission.groups.clear()

    def ban_member(self, user):
        user_admission = self._get_user_admission(user)
        user_admission.is_active = False
        user_admission.save()

    def unban_member(self, user):
        user_admission = self._get_user_admission(user)
        user_admission.is_active = True
        user_admission.save()

    def has_member(self, user):
        user_admission = self._get_user_admission(user)
        return user_admission.groups.count()

    def get_ban(self, user):
        user_admission = self._get_user_admission(user)
        return not user_admission.is_active

    """
    Group getters
    """

    def _is_group(self, user, group):
        user_admission = self._get_user_admission(user)
        return user_admission.groups.filter(name=group).exists()

    def is_director(self, user):
        return self._is_group(user, 'Director')

    def is_super_administrator(self, user):
        return self._is_group(user, 'Super-administrator')

    def is_administrator(self, user):
        return self._is_group(user, 'Administrator')

    def is_teacher(self, user):
        return self._is_group(user, 'Teacher')

    def is_client(self, user):
        return self._is_group(user, 'Client')

    """
    Group setters
    """

    def _set_group(self, user, group):
        group, created = Group.objects.get_or_create(name=group)
        user_admission = self._get_user_admission(user)
        user_admission.groups.add(group)

    def set_group_director(self, user):
        self._set_group(user, 'Director')
        self.set_group_super_administrator(user)

    def set_group_super_administrator(self, user):
        self._set_group(user, 'Super-administrator')
        self.set_group_administrator(user)

    def set_group_administrator(self, user):
        self._set_group(user, 'Administrator')

    def set_group_teacher(self, user):
        self._set_group(user, 'Teacher')

    def set_group_client(self, user):
        self._set_group(user, 'Client')
