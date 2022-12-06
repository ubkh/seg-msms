from django.contrib.auth.models import Group
from django.db import models


class Admission(models.Model):
    school = models.ForeignKey('School', on_delete=models.CASCADE)
    client = models.ForeignKey('User', on_delete=models.CASCADE, related_name='admission')
    groups = models.ManyToManyField(Group)
    is_active = models.BooleanField(default=True, verbose_name='Active Account')

    class Meta:
        unique_together = ('school', 'client')
