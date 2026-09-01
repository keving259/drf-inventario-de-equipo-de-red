#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate

# Crear superusuario si no existe
python manage.py createsuperuser --no-input || true

# Crea o actualiza usuario solo de lectura
python manage.py create_demo_user || true