FROM python:3-slim-stretch

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    mariadb-client \
    build-essential \
    iputils-ping && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir inventory

RUN pip install --no-cache-dir --trusted-host curl psycopg2-binary requests Flask wheel uwsgi

COPY . inventory

WORKDIR inventory

RUN ./build.sh

EXPOSE 8080

CMD ["./run.sh"]
