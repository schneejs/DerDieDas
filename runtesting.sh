#!/bin/sh

python manage.py flush --noinput
python manage.py loaddata testingdump.json
python manage.py runserver