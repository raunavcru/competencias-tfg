# competencias-tfg

## Instalación
- Intalación de Python3:
    https://www.python.org/downloads/
- Ejecutamos el siguiente comando:
    pip install virtualenvwrapper-win
- Creamos el entorno virtual:
    mkvirtualenv <NombreEntorno>
- Accedemos al entorno:
    workon <NombreEntorno>:
- Instalamos el archivo requirements.txt
    pip install -r requirements.txt
- Instalamos PostgresSQL:
    https://www.postgresql.org/download/
- Ejecutamos el siguiente comando:
    py manage.py migrate
- Creamos el super usuario:
    py manage.py createsuperuser
- Ejecutamos el servidor:
    py manage.py runserver

## Ramas
Ramas por defecto:
- master
- dev

En la rama **dev** se incluirán todas las ramas de desarrollo con *pull requests*. La rama **master** solo se podrán añadir desde la rama **dev**, para incluir la release. 

El resto de ramas seguirán el siguiente esquema:
*brach_code/sprint_code/task_code*

Códigos de rama:
- feat/     (nueva feature)
- fix/      (bug fix)
- hotfix/   (bug fixes en producción)
- refactor/ (refactorización de código)
- doc/      (cambios de documentación)
- test/     (añadir o refactorizar tests)
- release/  (nueva realise)
