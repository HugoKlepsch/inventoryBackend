FROM python:3-slim-stretch

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    mariadb-client \
    iputils-ping && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir inventory

RUN pip install --no-cache-dir --trusted-host curl requests Flask mysqlclient flask_sqlalchemy

COPY . inventory

WORKDIR inventory

RUN ./build.sh

EXPOSE 8080

CMD ["./run.sh"]
