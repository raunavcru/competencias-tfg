from django.contrib.auth.hashers import make_password
from django.core import management
from django.utils.crypto import get_random_string
from django.utils.timezone import now
from faker import Faker

from corrigeapp.models import Student, Teacher, Administrator

import random
import json

DATE_FORMAT = '%Y-%m-%d %H:%M:%S%z'
FAKE = Faker('es_ES')
POPULATE = []
ROLE_CHOICE = ['TEACHER', 'ADMIN']
USER_PKS = range(1, 10)
STUDENT_PKS = range(1, 11)



def run():
    management.call_command('flush', interactive=False)

    seed_users()
    seed_profiles()
    seed_students()

    students = Student.objects.all()
    students.delete()

    teachers = Teacher.objects.all()
    teachers.delete()

    admins = Administrator.objects.all()
    admins.delete()

    with open('initial_data/initial_data.json', 'w') as file:
        file.write(json.dumps(POPULATE, indent=4))

    management.call_command('loaddata', 'initial_data/initial_data')

def seed_users():
    for pk in USER_PKS:
        profile = FAKE.profile()
        names = profile['name'].split(' ')
        first_name = names[0]
        last_name = names[1]

        fields = {
            'password': make_password(profile['username']),
            'is_superuser': False,
            'username': profile['username'],
            'first_name': first_name,
            'last_name': last_name,
            'email': profile['mail'],
            'is_staff': False,
            'date_joined': now().strftime(DATE_FORMAT),
        }
        user = {
            'pk': pk,
            'model': 'auth.User',
            'fields': fields
        }

        POPULATE.append(user)

def seed_profiles():
    for user_pk in USER_PKS:
        role = random.choice(ROLE_CHOICE)
        if role == 'TEACHER':
            teacher = {
                'pk': user_pk,
                'model': 'corrigeapp.TEACHER',
                'fields': {
                    'profile_ptr_id': user_pk,
                }
            }
            POPULATE.append(teacher)

            profile = {
                'pk': user_pk,
                'model': 'corrigeapp.PROFILE',
                'fields': {
                    'birthdate': '1980-01-01',
                    'initials': get_random_string(length=3).upper(),
                    'role': 'TEACHER',
                    'user': user_pk,
                }
            }
            POPULATE.append(profile)
            
        else:
            admin = {
                'pk': user_pk,
                'model': 'corrigeapp.ADMINISTRATOR',
                'fields': {
                    'profile_ptr_id': user_pk,
                }
            }
            POPULATE.append(admin) 

            profile = {
                'pk': user_pk,
                'model': 'corrigeapp.PROFILE',
                'fields': {
                    'birthdate': '1980-01-01',
                    'initials': get_random_string(length=3).upper(),
                    'role': 'ADMIN',
                    'user': user_pk,
                }
            }
            POPULATE.append(profile)

def seed_students():
    for pk in STUDENT_PKS:
        profile = FAKE.profile()
        names = profile['name'].split(' ')
        name = names[0]
        surname = names[1]

        student = {
            'pk': pk,
            'model': 'corrigeapp.Student',
            'fields': {
                'name': name,
                'surname': surname,
                'birthdate': '1980-01-01',
                'initials': get_random_string(length=3).upper(),
            }
        }
        POPULATE.append(student)
            
        

        