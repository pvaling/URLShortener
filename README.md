# URL Shortener

For coding practice

## Features

- Pluggable storage backends
    - InMemory
    - SQLBackend
      - SQLite included
- Collision handling with tests and retries
- Basic tests for TDD approach
- PyCharm HTTP client examples
- Written with Fast API and SQLAlchemy
- Object-oriented design of Shortener
- Dockerfile

## Todo
- UI
- Kubernetes
- Terraform for Yandex cloud
- InMemory Cache
- Split tables for same url collapse (storage space optimization)


## Run

```shell
uvicorn --port 8000 app:app
```

## Docker build

```shell
docker build -f docker/backend.Dockerfile --tag shortener-backend .
```

```shell
docker run --publish 8080:8080 shortener-backend
```
