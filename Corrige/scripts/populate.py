from django.contrib.auth.hashers import make_password
from django.core import management
from django.utils.crypto import get_random_string
from django.utils.timezone import now
from faker import Faker

from corrigeapp.models import Student, Teacher, Administrator, Competence, Subject, Evaluation, Set

import random
import json

DATE_FORMAT = '%Y-%m-%d %H:%M:%S%z'
FAKE = Faker('es_ES')
POPULATE = []
USER_PKS = range(2, 10)
STUDENT_PKS = range(1, 30)


def run():
    management.call_command('flush', interactive=False)

    seed_users()
    seed_profiles()
    seed_admins()
    seed_students()
    seed_competences()
    seed_subjects()
    seed_evaluations()
    seed_sets()

    sets = Set.objects.all()
    sets.delete()

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

    evaluations = Evaluation.objects.all()
    evaluations.delete()

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

def seed_admins():
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
        'pk': 1,
        'model': 'auth.User',
        'fields': fields
    }

    POPULATE.append(user)
    admin = {
        'pk': 1,
        'model': 'corrigeapp.ADMINISTRATOR',
        'fields': {
            'profile_ptr_id': 1,
        }
    }
    POPULATE.append(admin)

    profile = {
        'pk': 1,
        'model': 'corrigeapp.PROFILE',
        'fields': {
            'birthdate': '1980-01-01',
            'initials': get_random_string(length=3).upper(),
            'role': 'ADMINISTRATOR',
            'user': 1,
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
                'name': 'Ciencias Sociales',
                'level': '5º',
                'grade': 'Primaria',
                'description': 'Ciencias Sociales',
                'competences': competencels, 
            }
    }
    POPULATE.append(subject)
    subject_pk += 1
    competencels = []
    subject = {
        'pk': subject_pk,
        'model': 'corrigeapp.Subject',
        'fields': {
                'name': 'Lengua Castellana y Literatura',
                'level': '5º',
                'grade': 'Primaria',
                'description': 'Lengua Castellana y Literatura',
                'competences': competencels, 
            }
    }
    POPULATE.append(subject)
    subject_pk += 1
    competencels = []
    subject = {
        'pk': subject_pk,
        'model': 'corrigeapp.Subject',
        'fields': {
                'name': 'Matemáticas',
                'level': '5º',
                'grade': 'Primaria',
                'description': 'Matemáticas',
                'competences': competencels, 
            }
    }
    POPULATE.append(subject)
    subject_pk += 1
    competencels = []
    subject = {
        'pk': subject_pk,
        'model': 'corrigeapp.Subject',
        'fields': {
                'name': 'Valores Sociales y Cívicos',
                'level': '5º',
                'grade': 'Primaria',
                'description': 'Valores Sociales y Cívicos',
                'competences': competencels, 
            }
    }
    POPULATE.append(subject)
    subject_pk += 1
    competencels = []
    subject = {
        'pk': subject_pk,
        'model': 'corrigeapp.Subject',
        'fields': {
                'name': 'Educación Plástica',
                'level': '5º',
                'grade': 'Primaria',
                'description': 'Educación Plástica',
                'competences': competencels, 
            }
    }
    POPULATE.append(subject)
    subject_pk += 1
    competencels = []
    subject = {
        'pk': subject_pk,
        'model': 'corrigeapp.Subject',
        'fields': {
                'name': 'Educación Musical',
                'level': '5º',
                'grade': 'Primaria',
                'description': 'Educación Musical',
                'competences': competencels, 
            }
    }
    POPULATE.append(subject)
    subject_pk += 1
    competencels = []
    subject = {
        'pk': subject_pk,
        'model': 'corrigeapp.Subject',
        'fields': {
                'name': 'Segunda Lengua Extranjera',
                'level': '5º',
                'grade': 'Primaria',
                'description': 'Segunda Lengua Extranjera',
                'competences': competencels, 
            }
    }
    POPULATE.append(subject)
    subject_pk += 1
    competencels = []
    subject = {
        'pk': subject_pk,
        'model': 'corrigeapp.Subject',
        'fields': {
                'name': 'Educación Física',
                'level': '5º',
                'grade': 'Primaria',
                'description': 'Educación Física',
                'competences': competencels, 
            }
    }
    POPULATE.append(subject)
    subject_pk += 1

def seed_evaluations():
    evaluation = {
        'pk': 1,
        'model': 'corrigeapp.Evaluation',
        'fields': {
                'name': 'Matemáticas 5º Primaria Final',
                'start_date': '1980-01-01',
                'end_date': '1980-01-01',
                'is_final': True,
                'period': 'Final',
                'subject': 3,
            }
    }
    POPULATE.append(evaluation)

def seed_sets():
    students = []

    for n in STUDENT_PKS:
        students.append(n)

    set_obj = {
        'pk': 1,
        'model': 'corrigeapp.Set',
        'fields': {
                'name': 'Matemáticas 5ºA Primaria',
                'level': '5º',
                'grade': 'Primaria',
                'line': 'A',
                'teacher': 2,
                'subject': 3,
                'evaluation': 1,
                'students': students,
            }
    }
    POPULATE.append(set_obj)