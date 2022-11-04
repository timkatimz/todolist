#!/bin/bash
python scr/manage.py makemigrations --check
status=$?
if [[ $status != 0 ]]; then
  python scr/manage.py makemigrations
  python scr/manage.py migrate
fi
exec "$@"