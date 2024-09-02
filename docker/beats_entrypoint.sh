#!/bin/sh

echo "--> Waiting for db to be ready"
./wait-for-it.sh db:5432

echo "--> Starting beats process"
celery -A social_media_api.tasks beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

