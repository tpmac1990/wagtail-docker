#!/bin/sh

# exit on error and print trace
set -xe

# ls -la /vol/
# ls -la /vol/web

# whoami

# python manage.py wait_for_db
# python manage.py collectstatic --noinput
# python manage.py migrate

# uwsgi --socket :9000 --workers 4 --master --enable-threads --module app.wsgi


# cd in to the wagtail app
cd app 
# set -xe
python manage.py migrate --noinput
gunicorn app.wsgi:application