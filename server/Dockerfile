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
    iputils-ping \
    curl && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir inventory

RUN mkdir -p inventory/sass && \
    curl -L https://github.com/sass/dart-sass/releases/download/1.22.3/dart-sass-1.22.3-linux-x64.tar.gz > ./inventory/sass/sass.tar.gz && \
    cd ./inventory/sass && \
    tar -xzvf ./sass.tar.gz && \
    rm ./sass.tar.gz

RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.34.0/install.sh | bash
ENV NVM_DIR="/root/.nvm"
RUN . "$NVM_DIR/nvm.sh" && nvm install 8.11.4
RUN pip install --no-cache-dir --trusted-host curl requests Flask flask_sqlalchemy psycopg2

COPY . inventory

WORKDIR inventory

RUN ./build.sh

EXPOSE 80

CMD ["./run.sh"]
