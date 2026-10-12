# ROAM

[![CI](https://github.com/anthony-barret/roam/actions/workflows/ci.yml/badge.svg)](https://github.com/anthony-barret/roam/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/anthony-barret/roam/branch/dev/graph/badge.svg)](https://codecov.io/gh/anthony-barret/roam)

Roam is a personal travel journal and travel management web application.

It allows users to keep track of the places they have visited, document their trips and memories, and maintain a
wishlist of destinations they would like to discover.

## Getting started

### Prerequisite

Make sure the following tools are installed:

- Docker
- Docker Compose

### Configuration

Create a `.env` file in the project root directory using `.env.example` as a template:

```shell
cp .env.example .env
```

Review the environment variables and adjust them to your local setup if necessary.

### Start the application

Run the startup script from the project root:

```shell
./start.sh
```

### Stop the application

To stop the containers, run:

```shell
docker compose down
```

This stops and removes the containers and networks created by Compose, but preserves named volumes by default.

To also remove the associated volumes, run:

```shell
docker compose down -v
```

Warning: Removing volumes may permanently delete persisted data, including the database contents.
