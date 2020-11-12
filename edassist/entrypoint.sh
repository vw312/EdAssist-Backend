#! /bin/bash
uwsgi --http :8000 --master --enable-threads --processes=5 \
    --env DJANGO_SETTINGS_MODULE=edassist.settings --vacuum --max-requests=5000 \
    --buffer-size=65535 --module edassist.wsgi:application