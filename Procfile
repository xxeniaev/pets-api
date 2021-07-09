release: python3 compose_django_project/manage.py migrate

web: gunicorn compose_django_project/core.wsgi --log-file -