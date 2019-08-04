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
    mkdir server

RUN mkdir -p server/sass && \
    curl -L https://github.com/sass/dart-sass/releases/download/1.22.3/dart-sass-1.22.3-linux-x64.tar.gz > ./server/sass/sass.tar.gz && \
    cd ./server/sass && \
    tar -xzvf ./sass.tar.gz && \
    rm ./sass.tar.gz


COPY requirements.txt ./
RUN python3 -m venv venv && . venv/bin/activate && pip install --no-cache-dir -r requirements.txt

WORKDIR /server

RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.34.0/install.sh | bash
ENV NVM_DIR="/root/.nvm"
RUN . "$NVM_DIR/nvm.sh" && nvm install 8.11.4
COPY package.json package-lock.json ./
RUN . "$NVM_DIR/nvm.sh" && npm install

COPY . ./

RUN ./build.sh

EXPOSE 80

WORKDIR /

CMD ["./server/run.sh"]
