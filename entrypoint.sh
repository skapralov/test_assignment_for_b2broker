#!/bin/sh

echo "Waiting for mysql..."
while ! nc -z db 3306; do
  sleep 0.1
done
echo "mysql started"

python manage.py migrate
python manage.py test
python manage.py runserver 0.0.0.0:8000