FROM postgres:17

# Install build dependencies and pgvector
RUN apt-get update \
    && apt-get install -y \
        build-essential \
        git \
        postgresql-server-dev-17 \
    && git clone --branch v0.8.0 https://github.com/pgvector/pgvector.git \
    && cd pgvector \
    && make \
    && make install \
    && cd .. \
    && rm -rf pgvector \
    && apt-get remove -y \
        build-essential \
        git \
        postgresql-server-dev-17 \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy custom initialization scripts
COPY ./init /docker-entrypoint-initdb.d/