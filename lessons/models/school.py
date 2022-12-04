"""
Models that will be used in the music school management system.
"""
from django.contrib.auth.models import Group
from django.db import models

from lessons.models import Term
from lessons.models import User

class AdmissionMixin:
    """
    Mixin that allows a school to add a client to a specified user.

    School Groups
    ┏━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃   Super-administrator  ┃
    ┃           ↓ (inherits) ┃
    ┃     Administrator      ┃
    ┃         Teacher        ┃
    ┃         Client         ┃
    ┗━━━━━━━━━━━━━━━━━━━━━━━━┛
    """

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
        on_delete=models.CASCADE
    )
    clients = models.ManyToManyField(
        User,
        through='Admission',
        related_name='enrolled_school'
    )


class Admission(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admission')
    groups = models.ManyToManyField(Group)
    is_active = models.BooleanField(default=True, verbose_name='Active Account')

    class Meta:
        unique_together = ('school', 'client')


