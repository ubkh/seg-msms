from django.core.management.base import BaseCommand
from lessons.models import User, Lesson, School, Term, Transfer, Admission


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("The database is unseeding...")
        User.objects.all().delete()
        Lesson.objects.all().delete()
        School.objects.all().delete()
        Term.objects.all().delete()
        Transfer.objects.all().delete()
        Admission.objects.all().delete()

