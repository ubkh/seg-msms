from django.core.management.base import BaseCommand
from lessons.models import User, Lesson, School, Term


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("The database is unseeding...")
        User.objects.all().delete()
        Lesson.objects.all().delete()
        School.objects.all().delete()
        Term.objects.all().delete()
