from django.contrib.auth.hashers import make_password
from django.core import management
from django.utils.crypto import get_random_string
from django.utils.timezone import now
from faker import Faker

from corrigeapp.models import Student, Teacher, Administrator, Competence, Subject

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
    seed_competences()
    seed_subjects()

    students = Student.objects.all()
    students.delete()

    teachers = Teacher.objects.all()
    teachers.delete()

    admins = Administrator.objects.all()
    admins.delete()

    competences = Competence.objects.all()
    competences.delete()

    subjects = Subject.objects.all()
    subjects.delete()

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

def seed_competences():
    competence_pk = 1

    ## Level 3
    competence = {
        'pk': competence_pk,
        'model': 'corrigeapp.Competence',
        'fields': {
                'code': 'CC1',
                'name': 'Comunicación lingüística',
                'description': 'Comunicación lingüística.',
                'level': 3,
            }
    }
    POPULATE.append(competence)
    competence_pk += 1

    ## Level 3
    competence = {
        'pk': competence_pk,
        'model': 'corrigeapp.Competence',
        'fields': {
                'code': 'CC2',
                'name': 'Competencia matemática y competencias básicas en ciencia y tecnología',
                'description': 'Competencia matemática y competencias básicas en ciencia y tecnología.',
                'level': 3,
            }
    }
    POPULATE.append(competence)
    competence_pk += 1

    ## Level 3
    competence = {
        'pk': competence_pk,
        'model': 'corrigeapp.Competence',
        'fields': {
                'code': 'CC3',
                'name': 'Competencia digital',
                'description': 'Competencia digital.',
                'level': 3,
            }
    }
    POPULATE.append(competence)
    competence_pk += 1

    ## Level 3
    competence = {
        'pk': competence_pk,
        'model': 'corrigeapp.Competence',
        'fields': {
                'code': 'CC4',
                'name': 'Aprender a aprender',
                'description': 'Aprender a aprender.',
                'level': 3,
            }
    }
    POPULATE.append(competence)
    competence_pk += 1

    ## Level 3 =====================================================================================
    competence = {
        'pk': competence_pk,
        'model': 'corrigeapp.Competence',
        'fields': {
                'code': 'CC5',
                'name': 'Competencias sociales y cívicas',
                'description': 'Competencias sociales y cívicas.',
                'level': 3,
            }
    }
    POPULATE.append(competence)
    competence_level3_pk = competence_pk
    competence_pk += 1
    ## Level 2
    competence = {
        'pk': competence_pk,
        'model': 'corrigeapp.Competence',
        'fields': {
                'code': 'CS1',
                'name': 'Obtener información concreta y relevante sobre hechos o fenómenos previamente delimitados, utilizando diferentes fuentes (directas e indirectas).',
                'description': 'Obtener información concreta y relevante sobre hechos o fenómenos previamente delimitados, utilizando diferentes fuentes (directas e indirectas).',
                'weight': 0.15,
                'level': 2,
                'parent': competence_level3_pk,
        }
    }
    POPULATE.append(competence)
    competence_level2_pk = competence_pk
    competence_pk += 1
    ## Level 1
    competence = {
        'pk': competence_pk,
        'model': 'corrigeapp.Competence',
        'fields': {
                'code': 'CS1.1',
                'name': 'Busca, selecciona y organiza información concreta y relevante, la analiza, obtiene conclusiones, reflexiona acerca del proceso seguido y lo comunica oralmente y/o por escrito.',
                'description': 'Busca, selecciona y organiza información concreta y relevante, la analiza, obtiene conclusiones, reflexiona acerca del proceso seguido y lo comunica oralmente y/o por escrito.',
                'weight': 0.15,
                'level': 1,
                'parent': competence_level2_pk,
        }
    }
    POPULATE.append(competence)
    competence_pk += 1
    ## Level 2
    competence = {
        'pk': competence_pk,
        'model': 'corrigeapp.Competence',
        'fields': {
                'code': 'CS2',
                'name': 'Utilizar las tecnologías de la información y la comunicación para obtener información aprender y expresar contenidos sobre Ciencias Sociales.',
                'description': 'Utilizar las tecnologías de la información y la comunicación para obtener información aprender y expresar contenidos sobre Ciencias Sociales.',
                'weight': 0.3,
                'level': 2,
                'parent': competence_level3_pk,
        }
    }
    POPULATE.append(competence)
    competence_level2_pk = competence_pk
    competence_pk += 1
    ## Level 1
    competence = {
        'pk': competence_pk,
        'model': 'corrigeapp.Competence',
        'fields': {
                'code': 'CS2.1',
                'name': 'Utiliza la tecnologías de la información y la comunicación (Internet, blogs, redes sociales…) para elaborar trabajos con la terminología adecuada a los temas tratados.',
                'description': 'Utiliza la tecnologías de la información y la comunicación (Internet, blogs, redes sociales…) para elaborar trabajos con la terminología adecuada a los temas tratados.',
                'weight': 0.15,
                'level': 1,
                'parent': competence_level2_pk,
        }
    }
    POPULATE.append(competence)
    competence_pk += 1

    ## Level 3
    competence = {
        'pk': competence_pk,
        'model': 'corrigeapp.Competence',
        'fields': {
                'code': 'CC6',
                'name': 'Sentido de la iniciativa y espíritu emprendedor',
                'description': 'Sentido de iniciativa y espíritu emprendedor.',
                'level': 3,
            }
    }
    POPULATE.append(competence)
    competence_pk += 1

    ## Level 3
    competence = {
        'pk': competence_pk,
        'model': 'corrigeapp.Competence',
        'fields': {
                'code': 'CC7',
                'name': 'Conciencia y expresiones culturales',
                'description': 'Conciencia y expresiones culturales.',
                'level': 3,
            }
    }
    POPULATE.append(competence)
    competence_pk += 1

def seed_subjects():
    subject_pk = 1
    competencels = []

    competencels = [5,6,7,8,9]
    subject = {
        'pk': subject_pk,
        'model': 'corrigeapp.Subject',
        'fields': {
                'name': 'Ciencias sociales',
                'level': '5º',
                'grade': 'Primaria',
                'description': 'Ciencias sociales',
                'competences': competencels, 
            }
    }
    POPULATE.append(subject)
    subject_pk += 1