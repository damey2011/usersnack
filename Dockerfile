FROM python:3.11.5-alpine3.18 as python-base
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    g++ libc-dev linux-headers postgresql-dev \
    && apk add libffi-dev curl
ENV POETRY_VERSION=1.7.1
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"
WORKDIR /app/

FROM python-base AS app
ENV PYTHONPATH=/app/src
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi
COPY . /app
EXPOSE 8000
CMD ["./scripts/entrypoint-api.sh"]
