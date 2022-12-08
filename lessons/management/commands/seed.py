from django.core.management.base import BaseCommand
import datetime
from faker import Faker
import random

from lessons.models import User, Lesson, School, Term, Transfer, Admission


class Command(BaseCommand):

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def create_lesson(self, student_user, teacher_user, school, term, fulfilled):
        lesson = Lesson.objects.create(
            title="Piano Lesson",
            instrument="Piano",
            teacher=teacher_user,
            day="Monday",
            time="03:00",
            interval="1",
            duration="30",
            information="I have no prior experience.",
            fulfilled=fulfilled,
            student=student_user,
            school=school,
        )
        return lesson

    def handle(self, *args, **options):
        print("The database is seeding...")

        INSTRUMENTS = [
            ('Piano', 'Piano'),
            ('Guitar','Guitar'),
            ('Drums','Drums'),
            ('Violin','Violin'),
            ('Trumpet','Trumpet'),
            ('Flute','Flute'),
            ('Harp','Harp'),
        ]

        Term.objects.all().delete()



        Transfer.objects.all().delete()
        Admission.objects.all().delete()


        User.objects.all().delete()
        # Create Director
        User.objects.filter(email="marty.major@example.org").delete()
        director_user = User.objects.create_user(
            email="marty.major@example.org",
            first_name="Marty",
            last_name="Major",
            password="Password123",
        )
        director_user.set_group_director()

        School.objects.all().delete()
        school, created = School.objects.get_or_create(
            name="King's Music School",
            director=director_user,
            description=self.faker.text(max_nb_chars=1000)
        )

        t = Term.objects.create(id=1,start_date=datetime.date(2022, 9, 1), end_date=datetime.date(2022, 10, 21), school=school)
        Term.objects.create(id=2,start_date=datetime.date(2022, 10, 31), end_date=datetime.date(2022, 12, 16), school=school)
        Term.objects.create(id=3,start_date=datetime.date(2023, 1, 3), end_date=datetime.date(2023, 2, 10), school=school)
        Term.objects.create(id=4,start_date=datetime.date(2023, 2, 20), end_date=datetime.date(2023, 3, 31), school=school)
        Term.objects.create(id=5,start_date=datetime.date(2023, 4, 17), end_date=datetime.date(2023, 5, 26), school=school)
        Term.objects.create(id=6,start_date=datetime.date(2023, 6, 5), end_date=datetime.date(2023, 7, 21), school=school)

        setattr(school, 'current_term', t)


        school.set_group_director(director_user)

        # Create Student
        User.objects.filter(email="john.doe@example.org").delete()
        student_user = User.objects.create_user(
            email="john.doe@example.org",
            first_name="John",
            last_name="Doe",
            password="Password123",
        )
        student_user.set_group_adult_user()
        school.set_group_client(student_user)

        alice_doe = User.objects.create_user(
            first_name="Alice",
            last_name="Doe",
            password="Password123",
            email="alice.doe@example.org",
            parent=student_user
        )

        bob_doe = User.objects.create_user(
            first_name="Bob",
            last_name="Doe",
            password="Password123",
            email="bob.doe@example.org",
            parent=student_user
        )

        # Create Administrator
        User.objects.filter(email="petra.pickles@example.org").delete()
        administrator_user = User.objects.create_user(
            email="petra.pickles@example.org",
            first_name="Petra",
            last_name="Pickles",
            password="Password123",
        )
        administrator_user.set_group_adult_user()
        school.set_group_administrator(administrator_user)

        # Create Teacher
        User.objects.filter(email="norma.noe@example.org").delete()
        teacher_user = User.objects.create_user(
            email="norma.noe@example.org",
            first_name="Norma",
            last_name="Noe",
            instrument=["Piano", "Violin"],
            password="Password123",
        )
        teacher_user.set_group_adult_user()
        teacher_user.set_group_director()
        school.set_group_teacher(teacher_user)
        l = self.create_lesson(student_user, teacher_user, school, t, True)
        Transfer.objects.create(user=student_user, lesson=l, school=school, amount=l.price)
        self.create_lesson(student_user, teacher_user, school, t, False)

        norma_school, created = School.objects.get_or_create(
            name="The Norma Noe School of Music",
            director=teacher_user,
            description=self.faker.text(max_nb_chars=1000)
        )

        t = Term.objects.create(id=7,start_date=datetime.date(2022, 9, 1), end_date=datetime.date(2022, 10, 21), school=norma_school)
        Term.objects.create(id=8,start_date=datetime.date(2022, 10, 31), end_date=datetime.date(2022, 12, 16), school=norma_school)
        Term.objects.create(id=9,start_date=datetime.date(2023, 1, 3), end_date=datetime.date(2023, 2, 10), school=norma_school)
        Term.objects.create(id=10,start_date=datetime.date(2023, 2, 20), end_date=datetime.date(2023, 3, 31), school=norma_school)
        Term.objects.create(id=11,start_date=datetime.date(2023, 4, 17), end_date=datetime.date(2023, 5, 26), school=norma_school)
        Term.objects.create(id=12,start_date=datetime.date(2023, 6, 5), end_date=datetime.date(2023, 7, 21), school=norma_school)

        setattr(norma_school, 'current_term', t)
        norma_school.set_group_director(teacher_user)
        norma_school.set_group_administrator(student_user)
        norma_school.set_group_client(administrator_user)


        l = self.create_lesson(alice_doe, teacher_user, school, t, True)
        Transfer.objects.create(user=student_user, lesson=l, school=school, amount=l.price)
        l = self.create_lesson(alice_doe, teacher_user, school, t, True)
        Transfer.objects.create(user=student_user, lesson=l, school=school, amount=l.price)





        teacher_list = []

        # Generate 10 random Teachers
        for i in range(10):
            first_name = self.faker.first_name()
            last_name = self.faker.last_name()
            email = f'{first_name}.{last_name}@{self.faker.domain_name()}'
            instrument = random.sample(INSTRUMENTS, k=random.randint(1, len(INSTRUMENTS)))
            password = User.objects.make_random_password()
            teacher_user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                instrument=instrument
            )
            teacher_list.append(teacher_user)
            print(f'Seeding Teacher User {i}', end='\r')
            teacher_user.set_group_adult_user()
            school.set_group_teacher(teacher_user)

            l = self.create_lesson(bob_doe, teacher_user, school, teacher_list[0], True)
            Transfer.objects.create(user=student_user, lesson=l, school=school, amount=l.price)
            l = self.create_lesson(bob_doe, teacher_user, school, teacher_list[0], True)
            Transfer.objects.create(user=student_user, lesson=l, school=school, amount=l.price)


        user_list = []
        # Generate 100 random students for kings school
        for i in range(100):
            first_name = self.faker.first_name()
            last_name = self.faker.last_name()
            email = f'{first_name}.{last_name}@{self.faker.domain_name()}'
            password = User.objects.make_random_password()
            student_user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )
            user_list.append(student_user)
            print(f'Seeding User {i}', end='\r')
            student_user.set_group_adult_user()
            school.set_group_client(student_user)
            if random.random() < 0.7:
                l = self.create_lesson(student_user, random.choice(teacher_list), school, t, True)
                amount_diff = [0, 0.5, 1, 2]
                diff = random.choice(amount_diff)
                Transfer.objects.create(user=student_user, lesson=l, school=school, amount=l.price*diff)
            if random.random() < 0.3:
                l = self.create_lesson(student_user, random.choice(teacher_list), school, t, False)

        # Generate random children per user for kings school
        for user in user_list:
            if random.random() < 0.6:
                first_name = self.faker.first_name()
                last_name = self.faker.last_name()
                student_user = User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    parent=user,
                    email=f'{first_name}.{last_name}@{self.faker.domain_name()}',
                    password="Password123"
                )
                student_user.set_group_user()
                school.set_group_client(student_user)
                if random.random() < 0.7:
                    l = self.create_lesson(student_user, random.choice(teacher_list), school, t, True)
                    amount_diff = [0, 0.5, 1, 2]
                    diff = random.choice(amount_diff)
                    Transfer.objects.create(user=student_user, lesson=l, school=school, amount=l.price * diff)
                if random.random() < 0.3:
                    l = self.create_lesson(student_user, random.choice(teacher_list), school, t, False)


        teacher_list = []

        # Generate 10 random Teachers
        for i in range(10):
            first_name = self.faker.first_name()
            last_name = self.faker.last_name()
            email = f'{first_name}.{last_name}@{self.faker.domain_name()}'
            instrument = random.sample(INSTRUMENTS, k=random.randint(1, len(INSTRUMENTS)))
            password = User.objects.make_random_password()
            teacher_user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                instrument=instrument
            )
            teacher_list.append(teacher_user)
            print(f'Seeding Teacher User {i}', end='\r')
            teacher_user.set_group_adult_user()
            norma_school.set_group_teacher(teacher_user)


        user_list = []
        # Generate 100 random students for norma school
        for i in range(100):
            first_name = self.faker.first_name()
            last_name = self.faker.last_name()
            email = f'{first_name}.{last_name}@{self.faker.domain_name()}'
            password = User.objects.make_random_password()
            student_user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )
            user_list.append(student_user)
            print(f'Seeding User {i}', end='\r')
            student_user.set_group_adult_user()
            norma_school.set_group_client(student_user)
            if random.random() < 0.7:
                l = self.create_lesson(student_user, random.choice(teacher_list), norma_school, t, True)
                amount_diff = [0, 0.5, 1, 2]
                diff = random.choice(amount_diff)
                Transfer.objects.create(user=student_user, lesson=l, school=norma_school, amount=l.price*diff)
            if random.random() < 0.3:
                l = self.create_lesson(student_user, random.choice(teacher_list), norma_school, t, False)

        # Generate random children per user for norma school
        for user in user_list:
            if random.random() < 0.6:
                first_name = self.faker.first_name()
                last_name = self.faker.last_name()
                student_user = User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    parent=user,
                    email=f'{first_name}.{last_name}@{self.faker.domain_name()}',
                    password="Password123"
                )
                student_user.set_group_user()
                norma_school.set_group_client(student_user)
                if random.random() < 0.7:
                    l = self.create_lesson(student_user, random.choice(teacher_list), norma_school, t, True)
                    amount_diff = [0, 0.5, 1, 2]
                    diff = random.choice(amount_diff)
                    Transfer.objects.create(user=student_user, lesson=l, school=norma_school, amount=l.price * diff)
                if random.random() < 0.3:
                    l = self.create_lesson(student_user, random.choice(teacher_list), norma_school, t, False)


        # Generate 1 random Admins
        for i in range(1):
            first_name = self.faker.first_name()
            last_name = self.faker.last_name()
            email = f'{first_name}.{last_name}@{self.faker.domain_name()}'
            password = User.objects.make_random_password()
            admin_user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )
            print(f'Seeding Admin User {i}', end='\r')
            admin_user.set_group_adult_user()
            school.set_group_administrator(admin_user)



        # Seed Database with Default Terms



        school.save()


