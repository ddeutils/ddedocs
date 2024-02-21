# Docker: _Dockerfile_

## Docker Init

!!! quote inline end

    The docker init makes dockerization a piece of cake, especially for the Docker
    newbies. It eliminates the manual task of writing Dockerfiles and other configuration
    files, saving time and minimizing errors.[^1]

`docker init` is a command-line utility that helps in the initialization of Docker
resources within a project. It creates Dockerfiles, Compose files, and `.dockerignore`
files based on the project’s requirements.

!!! note

    Latest version of `docker init` supports Go, Python, Node.js, Rust, ASP.NET,
    PHP, and Java. It is available with Docker Desktop.

## Multi-Stage Builds

=== "Python"

    ```dockerfile
    # temp stage
    FROM python:3.9-slim as builder

    WORKDIR /app

    ENV PYTHONDONTWRITEBYTECODE 1
    ENV PYTHONUNBUFFERED 1

    RUN apt-get update && \
        apt-get install -y --no-install-recommends gcc

    COPY requirements.txt .
    RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


    # final stage
    FROM python:3.9-slim

    WORKDIR /app

    COPY --from=builder /app/wheels /wheels
    COPY --from=builder /app/requirements.txt .

    RUN pip install --no-cache /wheels/*
    ```

## References

- [TestDriven: Tips - Docker multi-stage builds](https://testdriven.io/tips/6ef63d0e-f3b6-41f3-8127-ca5f0a55c43f/)

[^1]: [You should stop writing Dockerfiles today — Do this instead](https://medium.com/@akhilesh-mishra/you-should-stop-writing-dockerfiles-today-do-this-instead-3cd8a44cb8b0)
