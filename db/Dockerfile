FROM postgres:10

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y \
    iputils-ping && \
    mkdir inventory && \
    rm -rf /var/lib/apt/lists/*

ENV POSTGRES_PASSWORD="notwaterloo"
ENV POSTGRES_USER="root"
ENV POSTGRES_DB="inventorydb"

COPY . inventory

WORKDIR inventory

#EXPOSE 3306
EXPOSE 5432
