from django.core.management.base import BaseCommand, CommandError
from lessons.models import User
from django.contrib.auth.models import Group

from lessons.models.school import School


class Command(BaseCommand):

    def handle(self, *args, **options):
        print("NOTE: The seed command has not been FULLY implemented yet!")
        print("TO DO: Create a seed command following the instructions of the assignment carefully.")

        # temp
        school, created = School.objects.get_or_create(
            name = "KCL Kangaroos"
        )

        student_group, created = Group.objects.get_or_create(name='Student')
        administrator_group, created = Group.objects.get_or_create(name='Administrator')
        super_administrator_group, created = Group.objects.get_or_create(name='Super-administrator')
        director_group, created = Group.objects.get_or_create(name='Director')

        # Create Student
        User.objects.filter(email="john.doe@example.org").delete()
        student_user = User.objects.create_user(
            email="john.doe@example.org",
            first_name="John",
            last_name="Doe",
            password="Password123",
        )
        student_user.groups.add(student_group)

        # Create Administrator
        User.objects.filter(email="petra.pickles@example.org").delete()
        administrator_user = User.objects.create_user(
            email="petra.pickles@example.org",
            first_name="Petra",
            last_name="Pickles",
            password="Password123",
        )
        administrator_user.groups.add(administrator_group)

        # Create Director
        User.objects.filter(email="marty.major@example.org").delete()
        director_user = User.objects.create_user(
            email="marty.major@example.org",
            first_name="Marty",
            last_name="Major",
            password="Password123",
        )
        director_user.groups.add(director_group)
        director_user.groups.add(super_administrator_group)
        director_user.groups.add(administrator_group)
