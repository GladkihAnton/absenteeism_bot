#!/usr/bin/env bash

# Predefined values
SRV_PORT=8000
DATA_PATH=fixtures/*.json
# -----------------

for argument in "$@"; do
  case $argument in
    -mm | --makemigrations)
      printf "Makemigrations \n\n"
      python manage.py makemigrations
      ;;

    -m | --migrate)
      printf "Migrate \n\n"
      python manage.py migrate
      ;;


    -l | --loaddata)
      printf "Load data...\n\n"
      python manage.py loaddata ${DATA_PATH}
      ;;

    *)
      echo "Unknown argument"
    ;;
  esac
done

echo "Start Gift admin, listening port $SRV_PORT..."
python manage.py runserver 0.0.0.0:${SRV_PORT}
