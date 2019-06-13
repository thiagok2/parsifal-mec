#!/bin/bash

echo "======>>>python /app/manage.py migrate auth"
python /app/manage.py migrate auth

echo "======>>>python /app/manage.py migrate reviews"
python /app/manage.py migrate reviews --noinput


echo "======>>>python /app/manage.py syncdb"
python /app/manage.py syncdb --noinput

echo "======>>>python /app/manage.py loaddata source_initial_data.json"
python /app/manage.py loaddata source_initial_data.json

echo "======>>>python /app/manage.py runserver 0.0.0.0:8000"
python /app/manage.py runserver 0.0.0.0:8000
