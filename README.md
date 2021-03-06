# AMRC OWAST

[![Build Status](https://dev.azure.com/sheffielduni/owast/_apis/build/status/owast?branchName=master)](https://dev.azure.com/sheffielduni/owast/_build/latest?definitionId=1&branchName=master)

Metadata registry, data store and web app.

# Installation

```bash
docker compose build --pull
docker scan owast_app
```

# Usage

```bash
curl --head http://localhost
```

## Service management

```bash
# Run services (The default argument is --file docker-compose.yaml)
docker-compose up -d
```

Logs

```bash
docker-compose logs --tail 100 -ft
```

## MongoDB shell

This allows direct access to the NoSQL database shell:

```bash
docker-compose exec meta mongosh
```

The PyMongo shell can be used to help develop the application:

```bash
docker-compose exec app python
```

Then run: (see the [PyMongo tutorial](https://pymongo.readthedocs.io/))

```python
import os
import pymongo

client = pymongo.MongoClient(os.environ['MONGO_URI'])
database = client.owast
collection = db.schemas
schema = collection.find_one()
```

# Maintenance

Check out outdated packages

```bash
docker-compose exec app pip list --outdated
```