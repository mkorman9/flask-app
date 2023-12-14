#!/usr/bin/env bash

sed -i "s/%HTTP_PORT%/${HTTP_PORT:-8080}/g" /etc/nginx/nginx.conf && \
  nginx && \
  exec uwsgi --ini uwsgi.ini --processes=${UWSGI_WORKERS:-8}
