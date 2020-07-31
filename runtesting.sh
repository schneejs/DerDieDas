#!/bin/sh

python manage.py flush --settings derdiedas.development --noinput
python manage.py loaddata --settings derdiedas.development testingdump.json
python manage.py runserver --settings derdiedas.development
