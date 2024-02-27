#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# python manage.py collectstatic --no-input

python3 manage.py makemigrations
python3 manage.py migrate

python3 manage.py makemigrations snippify
python3 manage.py migrate snippify
python3 manage.py migrate --run-syncdb

source '.env' && python manage.py createsuperuser --name=admin --email=admin@mail.com --noinput