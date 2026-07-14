# ivt-py

A small whoami-style Flask service that echoes request metadata and headers. It is useful for validating reverse proxy, ingress, container, and CI/CD configuration.

## App

The app is defined in `app.py` and exposes these routes:

```text
GET /      plain text request metadata
GET /ip    plain text request metadata
GET /json  JSON request metadata
```

The Docker runtime assumes the app entrypoint is `app:app`, which means `app.py` contains a Python object named `app`. Override this with `APP_MODULE` if another project uses a different entrypoint.

## Poetry

Install dependencies and run the app:

```bash
poetry install
poetry run gunicorn --bind 0.0.0.0:8000 app:app
```

Dev dependencies include `pytest`, `ruff`, and `pip-audit`. Install them with the default `poetry install`; the Docker `dev` and `test` targets install them with `poetry install --with dev`.

Run validation:

```bash
poetry check --lock
poetry run ruff check .
poetry run pip-audit
poetry run pytest
```

## Dockerfile

The root `Dockerfile` is a reusable Poetry Dockerfile with multiple targets:

```text
base     Python, Poetry, and project metadata
deps     runtime dependencies only
dev      dev dependencies and source code
test     dev image plus validation commands
runtime  production runtime image
```

Build targets:

```bash
docker build --target base -t ivt-py:base .
docker build --target deps -t ivt-py:deps .
docker build --target dev -t ivt-py:dev .
docker build --target test -t ivt-py:test .
docker build --target runtime -t ivt-py:runtime .
```

Run the runtime image:

```bash
docker run --rm -p 8000:8000 ivt-py:runtime
```

Override the app entrypoint or port:

```bash
docker run --rm -p 8000:8000 -e APP_MODULE=main:app ivt-py:runtime
docker run --rm -p 9000:9000 -e PORT=9000 ivt-py:runtime
```

## CI Images

The GitHub Actions workflow builds and scans the `dev` and `runtime` targets, builds the `test` target for validation, and publishes images from `main` or `v*.*.*` tags.

Runtime images are tagged with:

```text
latest
sha-<commit>
<version>
<major>.<minor>
<major>
```

Version tags come from Git tags, not package-manager metadata. For example, pushing `v1.2.3` publishes runtime tags `1.2.3`, `1.2`, and `1`.

The dev image is published as `dev`.
