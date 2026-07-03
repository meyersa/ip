FROM python:3-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.5 \
    POETRY_VIRTUALENVS_CREATE=false
ARG POETRY_INSTALL_ARGS="--only main"

# Install deps
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"
COPY pyproject.toml poetry.lock /app/
RUN poetry install $POETRY_INSTALL_ARGS --no-interaction --no-ansi --no-root

# Actual app
COPY . /app/

# Run Server
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
