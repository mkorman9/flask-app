FROM python:3.12-slim-bookworm

RUN apt -y update && \
	apt -y install build-essential nginx && \
	pip install uWSGI==2.0.23 && \
	apt -y remove build-essential gcc make g++ libc6-dev dpkg-dev subversion mercurial && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /runtime
EXPOSE 8080

COPY --chown=www-data:www-data webapp /runtime/webapp/
COPY --chown=www-data:www-data requirements.txt /runtime/requirements.txt

COPY --chmod=544 .docker/entrypoint.sh /runtime/entrypoint.sh
COPY .docker/uwsgi.ini /runtime/uwsgi.ini
COPY .docker/nginx.conf /etc/nginx/nginx.conf

RUN pip install -r requirements.txt

CMD ["./entrypoint.sh"]
