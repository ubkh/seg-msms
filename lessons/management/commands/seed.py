from django.core.management.base import BaseCommand, CommandError
from lessons.models import User, Term
from django.contrib.auth.models import Group
import datetime


class Command(BaseCommand):

    def handle(self, *args, **options):
        print("NOTE: The seed command has not been FULLY implemented yet!")
        print("TO DO: Create a seed command following the instructions of the assignment carefully.")

        # student_group, created = Group.objects.get_or_create(name='Student')
        # administrator_group, created = Group.objects.get_or_create(name='Administrator')
        # super_administrator_group, created = Group.objects.get_or_create(name='Super-administrator')
        # director_group, created = Group.objects.get_or_create(name='Director')

        # Create Student
        User.objects.filter(email="john.doe@example.org").delete()
        student_user = User.objects.create_user(
            email="john.doe@example.org",
            first_name="John",
            last_name="Doe",
            password="Password123",
        )
        student_user.set_group_student()
        # student_user.groups.add(student_group)

        # Create Administrator
        User.objects.filter(email="petra.pickles@example.org").delete()
        administrator_user = User.objects.create_user(
            email="petra.pickles@example.org",
            first_name="Petra",
            last_name="Pickles",
            password="Password123",
        )
        administrator_user.set_group_administrator()
        # administrator_user.groups.add(administrator_group)

        # Create Director
        User.objects.filter(email="marty.major@example.org").delete()
        director_user = User.objects.create_user(
            email="marty.major@example.org",
            first_name="Marty",
            last_name="Major",
            password="Password123",
        )
        director_user.set_group_director()
        # director_user.groups.add(director_group)
        # director_user.groups.add(super_administrator_group)
        # director_user.groups.add(administrator_group)

        Term.objects.all().delete()
        
        # Seed Database with Default Terms
        Term.objects.create(id=1,start_date=datetime.date(2022, 9, 1), end_date=datetime.date(2022, 10, 21))

        Term.objects.create(id=2,start_date=datetime.date(2022, 10, 31), end_date=datetime.date(2022, 12, 16))

        Term.objects.create(id=3,start_date=datetime.date(2023, 1, 3), end_date=datetime.date(2023, 2, 10))

        Term.objects.create(id=4,start_date=datetime.date(2023, 2, 20), end_date=datetime.date(2023, 3, 31))

        Term.objects.create(id=5,start_date=datetime.date(2023, 4, 17), end_date=datetime.date(2023, 5, 26))

        Term.objects.create(id=6,start_date=datetime.date(2023, 6, 5), end_date=datetime.date(2023, 7, 21))