from django.contrib.auth.hashers import make_password
from django.core import management
from django.utils.crypto import get_random_string
from django.utils.timezone import now
from faker import Faker

from corrigeapp.models import Student, Teacher, Administrator, Competence

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
    seed_competences_level3()
    seed_competences_level2()

    students = Student.objects.all()
    students.delete()

    teachers = Teacher.objects.all()
    teachers.delete()

    admins = Administrator.objects.all()
    admins.delete()

    competences = Competence.objects.all()
    competences.delete()

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

def seed_competences_level3():
    competence = {
        'pk': 1,
        'model': 'corrigeapp.Competence',
        'fields': {
                'code': 'CC1',
                'name': 'Comunicación lingüística',
                'description': 'Comunicación lingüística.',
                'level': 3,
            }
    }
    POPULATE.append(competence)
    competence = {
        'pk': 2,
        'model': 'corrigeapp.Competence',
        'fields': {
                'code': 'CC2',
                'name': 'Competencia matemática y competencias básicas en ciencia y tecnología',
                'description': 'Competencia matemática y competencias básicas en ciencia y tecnología.',
                'level': 3,
            }
    }
    POPULATE.append(competence)
    competence = {
        'pk': 3,
        'model': 'corrigeapp.Competence',
        'fields': {
                'code': 'CC3',
                'name': 'Competencia digital',
                'description': 'Competencia digital.',
                'level': 3,
            }
    }
    POPULATE.append(competence)
    competence = {
        'pk': 4,
        'model': 'corrigeapp.Competence',
        'fields': {
                'code': 'CC4',
                'name': 'Aprender a aprender',
                'description': 'Aprender a aprender.',
                'level': 3,
            }
    }
    POPULATE.append(competence)
    competence = {
        'pk': 5,
        'model': 'corrigeapp.Competence',
        'fields': {
                'code': 'CC5',
                'name': 'Competencias sociales y cívicas',
                'description': 'Competencias sociales y cívicas.',
                'level': 3,
            }
    }
    POPULATE.append(competence)
    competence = {
        'pk': 6,
        'model': 'corrigeapp.Competence',
        'fields': {
                'code': 'CC6',
                'name': 'Sentido de la iniciativa y espíritu emprendedor',
                'description': 'Sentido de iniciativa y espíritu emprendedor.',
                'level': 3,
            }
    }
    POPULATE.append(competence)
    competence = {
        'pk': 7,
        'model': 'corrigeapp.Competence',
        'fields': {
                'code': 'CC7',
                'name': 'Conciencia y expresiones culturales',
                'description': 'Conciencia y expresiones culturales.',
                'level': 3,
            }
    }
    POPULATE.append(competence)

def seed_competences_level2():    
    competence = {
        'pk': 8,
        'model': 'corrigeapp.Competence',
        'fields': {
                'code': 'CS1',
                'name': 'Obtener información concreta y relevante sobre hechos o fenómenos previamente delimitados, utilizando diferentes fuentes (directas e indirectas).',
                'description': 'Obtener información concreta y relevante sobre hechos o fenómenos previamente delimitados, utilizando diferentes fuentes (directas e indirectas).',
                'weight': 0.15,
                'level': 2,
                'parent': 5,
        }
    }
    POPULATE.append(competence)