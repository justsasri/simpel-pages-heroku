release: bash ./release.sh
web: gunicorn example.wsgi
worker: python manage.py rqworker default
