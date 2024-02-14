# Docker: _Dockerfile_

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
