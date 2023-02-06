#!/bin/bash

python3 ./manage.py flush --no-input
python3 ./manage.py makemigrations
python3 ./manage.py migrate
python3 ./manage.py collectstatic --noinput
python3 ./src/main/services/scrape_meal_api.py
