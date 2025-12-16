#!/bin/bash
pip install -r requirements.txt
python manage.py collectstatic --noinput --ignore admin
python manage.py migrate --noinput
