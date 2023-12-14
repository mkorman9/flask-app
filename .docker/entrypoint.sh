#!/usr/bin/env bash

sed -i "s/%HTTP_PORT%/${HTTP_PORT:-8080}/g" /etc/nginx/nginx.conf && \
  nginx && \
  exec uwsgi \
    --module=webapp.app \
    --callable=app \
    --socket="/tmp/uwsgi.sock" \
    --chmod-socket=666 \
    --chown-socket=www-data:www-data \
    --uid www-data \
    --gid www-data \
    --master \
    --processes=${UWSGI_WORKERS:-8} \
    --pidfile=/var/run/uwsgi-master.pid \
    --die-on-term \
    --exit-on-reload \
    --vacuum \
    --disable-logging
