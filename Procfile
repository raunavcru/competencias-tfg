release: sh -c 'cd Corrige && python manage.py migrate'
generatestatics: sh -c 'cd Corrige && python manage.py collectstatic'
web: sh -c 'cd Corrige && gunicorn Corrige.wsgi --log-file -'