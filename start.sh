#!/usr/bin/env bash

python manage.py migrate --noinput
python manage.py collectstatic --noinput
python config/create_superuser.py
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT