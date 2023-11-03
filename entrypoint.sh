#!/bin/bash

if [ "$1" = 'api' ] || [ $# -eq 0 ]; then
  set -e
  python -m alembic upgrade head
  exec python main.py
fi

eval "$@"