FROM python:3.12-slim-bookworm

RUN adduser --disabled-login --no-create-home --shell /bin/false --gecos "" gunicorn

WORKDIR /runtime
EXPOSE 8080

COPY --chown=gunicorn:gunicorn webapp /runtime/webapp/
COPY --chown=gunicorn:gunicorn requirements.txt /runtime/requirements.txt

RUN pip install -r requirements.txt

CMD exec python -m gunicorn \
    --workers ${WORKERS_COUNT:-4} \
    --bind "0.0.0.0:${HTTP_PORT:-8080}" \
    --user gunicorn --group gunicorn \
    --log-level error \
    webapp.app:app
