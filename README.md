# ip

A small whoami-style HTTP service that echoes request metadata and headers used to validate configuration and CI/CD. 

## Dev Container

The dev container uses the root `Dockerfile` with dev dependencies enabled.

Open the project with VS Code's **Dev Containers: Reopen in Container** command, or use the Dev Containers CLI:

```bash
devcontainer up --workspace-folder .
devcontainer exec --workspace-folder . poetry run pytest
devcontainer exec --workspace-folder . poetry run gunicorn --bind 0.0.0.0:8000 app:app
```

Port `8000` is forwarded by the dev container.

## Docker

The runtime Docker image installs dependencies with Poetry inside the image, so Poetry is not required on the host:

```bash
docker build -t ip .
docker run --rm -p 8000:8000 ip
```
