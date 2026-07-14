FROM python:3.14-slim AS base
WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=2.4.1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PORT=8000

RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

COPY pyproject.toml poetry.lock ./

FROM base AS deps
RUN poetry install --only main --no-interaction --no-ansi --no-root

FROM base AS dev
RUN poetry install --with dev --no-interaction --no-ansi --no-root
COPY . /app/

FROM dev AS test
RUN poetry check --lock \
    && poetry run ruff check . \
    && poetry run pip-audit \
    && poetry run pytest

FROM deps AS runtime
COPY . /app/

EXPOSE 8000
CMD ["sh", "-c", "exec poetry run gunicorn --bind \"0.0.0.0:${PORT}\" \"${APP_MODULE:-app:app}\""]
