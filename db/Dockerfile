FROM mysql:latest

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y \
    iputils-ping && \
    mkdir inventory && \
    rm -rf /var/lib/apt/lists/*

ENV MYSQL_ROOT_PASSWORD="notwaterloo"
ENV MYSQL_DATABASE="inventorydb"

COPY . inventory

WORKDIR inventory

EXPOSE 3306

RUN cp db.sql /docker-entrypoint-initdb.d/
