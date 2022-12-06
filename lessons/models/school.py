"""
Models that will be used in the music school management system.
"""
from django.contrib.auth.models import Group
from django.db import models
from datetime import datetime

from lessons.models import Term
from lessons.models import User


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

    def has_member(self, user):
        user_admission, created = Admission.objects.get_or_create(school=self, client=user)
        return user_admission.groups.count()

    def leave_school(self, user):
        user_admission, created = Admission.objects.get_or_create(school=self, client=user)
        user_admission.groups.clear()

    def ban_member(self, user):
        user_admission, created = Admission.objects.get_or_create(school=self, client=user)
        user_admission.is_active = False
        user_admission.save()

    def unban_member(self, user):
        user_admission, created = Admission.objects.get_or_create(school=self, client=user)
        user_admission.is_active = True
        user_admission.save()

    def get_ban(self, user):
        user_admission, created = Admission.objects.get_or_create(school=self, client=user)
        return not user_admission.is_active

    def is_director(self, user):
        user_admission, created = Admission.objects.get_or_create(school=self, client=user)
        return user_admission.groups.filter(name='Director').exists()

    def is_super_administrator(self, user):
        user_admission, created = Admission.objects.get_or_create(school=self, client=user)
        return user_admission.groups.filter(name='Super-administrator').exists()

    def is_administrator(self, user):
        user_admission, created = Admission.objects.get_or_create(school=self, client=user)
        return user_admission.groups.filter(name='Administrator').exists()

    def is_teacher(self, user):
        user_admission, created = Admission.objects.get_or_create(school=self, client=user)
        return user_admission.groups.filter(name='Teacher').exists()

    def is_client(self, user):
        user_admission, created = Admission.objects.get_or_create(school=self, client=user)
        return user_admission.groups.filter(name='Client').exists()

    def set_group_director(self, user):
        director_group, created = Group.objects.get_or_create(name='Director')
        user_admission, created = Admission.objects.get_or_create(school=self, client=user)
        user_admission.groups.add(director_group)
        self.set_group_super_administrator(user)

    def set_group_super_administrator(self, user):
        super_administrator_group, created = Group.objects.get_or_create(name='Super-administrator')
        user_admission, created = Admission.objects.get_or_create(school=self, client=user)
        user_admission.groups.add(super_administrator_group)
        self.set_group_administrator(user)

    def set_group_administrator(self, user):
        administrator_group, created = Group.objects.get_or_create(name='Administrator')
        user_admission, created = Admission.objects.get_or_create(school=self, client=user)
        user_admission.groups.add(administrator_group)

    def set_group_teacher(self, user):
        teacher_group, created = Group.objects.get_or_create(name='Teacher')
        user_admission, created = Admission.objects.get_or_create(school=self, client=user)
        user_admission.groups.add(teacher_group)

    def set_group_client(self, user):
        client_group, created = Group.objects.get_or_create(name='Client')
        user_admission, created = Admission.objects.get_or_create(school=self, client=user)
        user_admission.groups.add(client_group)


# more needs to be added


class School(AdmissionMixin, models.Model):
    """
    The School model holds shared state for a particular school.
    """
    name = models.CharField(max_length=30, blank=False)
    director = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        related_name='managed_school'
    )
    current_term = models.ForeignKey(
        Term,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='+'
    )
    clients = models.ManyToManyField(
        User,
        through='Admission',
        related_name='enrolled_school'
    )
    description = models.CharField(max_length=1000)

    @property
    def get_update_current_term(self):
        if self.current_term:
            if datetime.now().date() > self.current_term.end_date:
                next = Term.get_next_by_start_date(self.current_term)
                self.current_term = next
        return self.current_term


class Admission(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admission')
    groups = models.ManyToManyField(Group)
    is_active = models.BooleanField(default=True, verbose_name='Active Account')

    class Meta:
        unique_together = ('school', 'client')
