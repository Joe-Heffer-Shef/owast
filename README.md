# AMRC OWAST

Metadata registry, data store and web app.

# Installation

```bash
docker compose build --pull
docker scan owast_app
```

# Usage

```bash
curl --head http://localhost:8000
```

## Service management

```bash
# Run services (The default argument is --file docker-compose.yaml)
docker-compose up -d
```

## MongoDB shell

```bash
docker-compose exec meta mongosh
```

