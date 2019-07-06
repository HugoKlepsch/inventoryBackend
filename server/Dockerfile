FROM python:3-slim-stretch

# https://github.com/dalibo/temboard/commit/ff98d6740ae11345658508b02052294d6cffd448
RUN mkdir -p /usr/share/man/man1 && \
    mkdir -p /usr/share/man/man7 && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    mariadb-client \
    build-essential \
    postgresql-client \
    libpq-dev \
    iputils-ping && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir inventory

RUN pip install --no-cache-dir --trusted-host curl requests Flask flask_sqlalchemy psycopg2

COPY . inventory

WORKDIR inventory

RUN ./build.sh

EXPOSE 8080

CMD ["./run.sh"]
