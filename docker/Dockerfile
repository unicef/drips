FROM python:3.14-slim-bookworm AS base_os
ARG GOSU_VERSION=1.17
ARG GOSU_SHA256=bbc4136d03ab138b1ad66fa4fc051bafc6cc7ffae632b069a53657279a450de3
ARG BUILD_DATE
ARG VERSION
ARG SOURCE_COMMIT

RUN set -x \
  && runtimeDeps=" \
    libmagic1 \
    libxml2 \
    tini \
  " \
  && apt-get update \
  && apt-get install -y --no-install-recommends $runtimeDeps \
  && rm -rf /var/lib/apt/lists/* /var/cache/apt/*

RUN set -eux \
  && savedAptMark="$(apt-mark showmanual)" \
  && apt-get update \
  && apt-get install -y --no-install-recommends ca-certificates gnupg wget \
  && dpkgArch="$(dpkg --print-architecture | awk -F- '{ print $NF }')" \
  && wget -O /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch" \
  && wget -O /usr/local/bin/gosu.asc "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch.asc" \
  && export GNUPGHOME="$(mktemp -d)" \
  && gpg --batch --keyserver hkps://keys.openpgp.org --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4 \
  && gpg --batch --verify /usr/local/bin/gosu.asc /usr/local/bin/gosu \
  && gpgconf --kill all \
  && rm -rf "$GNUPGHOME" /usr/local/bin/gosu.asc \
  && apt-mark auto '.*' > /dev/null \
  && [ -z "$savedAptMark" ] || apt-mark manual $savedAptMark \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && chmod +x /usr/local/bin/gosu \
  && gosu --version \
  && rm -rf /var/lib/apt/lists/* /var/cache/apt/*

RUN groupadd --gid 1024 unicef \
    && adduser --disabled-login --disabled-password --no-create-home --ingroup unicef -q drips


# ------- builder -------
FROM base_os AS builder
RUN set -x \
    && buildDeps="build-essential \
cmake \
curl \
gcc \
git \
libssl-dev \
libxml2-dev \
python3-dev \
zlib1g-dev" \
    && apt-get update \
    && apt-get install -y --no-install-recommends $buildDeps gnupg unzip \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/*

RUN pip install uv uwsgi

# ------- tests -------
FROM builder AS tests
ARG BUILD_DATE
ARG VERSION
ARG SOURCE_COMMIT

LABEL distro="tests"
LABEL org.opencontainers.image.created="$BUILD_DATE"
LABEL org.opencontainers.image.version="$VERSION"

ENV PATH=/venv/bin:/usr/local/bin/:/usr/bin:/bin \
    DJANGO_SETTINGS_MODULE=drips.config.settings \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_PROJECT_ENVIRONMENT=/venv \
    VIRTUAL_ENV=/venv \
    UWSGI_PROCESSES=4

WORKDIR /app
COPY uv.lock README.rst MANIFEST.in pyproject.toml /app/
COPY src /app/src/

RUN --mount=type=cache,target=/root/.uv-cache \
    uv sync --cache-dir=/root/.uv-cache \
        --python=/usr/local/bin/python \
        --python-preference=system \
        --frozen

# ------- production only deps-------
FROM base_os AS production
RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/*
RUN pip install uv uwsgi
ENV PATH=/venv/bin:/usr/local/bin/:/usr/bin:/bin \
    DJANGO_SETTINGS_MODULE=drips.config.settings \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_PROJECT_ENVIRONMENT=/venv \
    VIRTUAL_ENV=/venv \
    UWSGI_PROCESSES=4

WORKDIR /app
COPY uv.lock README.rst MANIFEST.in pyproject.toml /app/
COPY src /app/src/

RUN --mount=type=cache,target=/root/.uv-cache \
    uv sync --cache-dir=/root/.uv-cache \
        --python=/usr/local/bin/python \
        --python-preference=system \
        --frozen



# ------- dist -------
FROM base_os AS dist
ARG BUILD_DATE
ARG GIT_SHA
ARG BRANCH
ARG VERSION
ARG GITHUB_SERVER_URL=https://github.com
ARG GITHUB_REPOSITORY=unicef/drips
ENV VERSION=$VERSION

ENV PATH=/venv/bin:/usr/local/bin/:/usr/bin:/bin \
    BUILD_DATE=$BUILD_DATE \
    SOURCE_COMMIT=$SOURCE_COMMIT \
    VERSION=$VERSION \
    BRANCH=$BRANCH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    STATIC_URL="/static/" \
    PYTHONPATH="" \
    PGSSLCERT="/tmp/postgresql.crt" \
    DJANGO_SETTINGS_MODULE=drips.config.settings \
    UV_PROJECT_ENVIRONMENT=/venv \
    VIRTUAL_ENV=/venv \
    UWSGI_PROCESSES=4

RUN <<EOF cat> /RELEASE
{"version": "$VERSION",
 "commit": "$SOURCE_COMMIT",
 "date": "$BUILD_DATE",
}
EOF
WORKDIR /app
COPY --chown=drips:unicef docker/conf /conf/
COPY docker/bin/* /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

COPY --chown=drips:unicef --from=production /venv /venv
COPY --from=builder /usr/local/bin/uwsgi /usr/local/bin/uv /usr/local/bin/
COPY --chown=drips:unicef src /app/src/
COPY --chown=drips:unicef uv.lock README.rst MANIFEST.in pyproject.toml /app/
RUN --mount=type=cache,target=/root/.uv-cache \
    uv --cache-dir=/root/.uv-cache  pip install --no-deps -e .
RUN chown drips:unicef /app

EXPOSE 8000
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["run"]


LABEL maintainer="drips@unicef.org"
LABEL org.opencontainers.image.authors="drips@unicef.org"
LABEL org.opencontainers.image.description="DRIPS - Donor Reporting Portal"
LABEL org.opencontainers.image.documentation="https://github.com/unicef/drips/"
LABEL org.opencontainers.image.title="DRIPS"
LABEL org.opencontainers.image.licenses="${GITHUB_SERVER_URL}/${GITHUB_REPOSITORY}/blob/${SOURCE_COMMIT:-master}/LICENSE"
LABEL org.opencontainers.image.revision=$SOURCE_COMMIT
LABEL org.opencontainers.image.source="${GITHUB_SERVER_URL}/${GITHUB_REPOSITORY}/tree/${SOURCE_COMMIT:-master}/"
LABEL org.opencontainers.image.url="https://hub.docker.com/repository/docker/unicef/drips/tags/"
LABEL org.opencontainers.image.vendor="UNICEF"
LABEL org.opencontainers.image.created="$BUILD_DATE"
LABEL org.opencontainers.image.version="$VERSION"
