FROM python:3.12-bookworm

RUN apt -y update && \
	apt -y install build-essential && \
	pip install uWSGI==2.0.23 && \
	apt -y remove build-essential gcc make g++ libc6-dev dpkg-dev subversion mercurial && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*
RUN adduser --disabled-login --no-create-home --shell /bin/false --gecos "" runner

WORKDIR /runtime
EXPOSE 8080

COPY --chown=runner:runner webapp /runtime/webapp/
COPY --chown=runner:runner requirements.txt /runtime/requirements.txt

RUN pip install -r requirements.txt

CMD exec uwsgi --http="${HTTP_HOST}:${HTTP_PORT:-8080}" --module=webapp.app --callable=app \
    --master --processes=${UWSGI_WORKERS:-8} --harakiri=${UWSGI_TIMEOUT:-60} --pidfile=/var/run/uwsgi-master.pid \
    --uid runner --gid runner \
    --die-on-term --vacuum
