# FastAPI beyond CRUD

# https://jod35.github.io/fastapi-beyond-crud-docs/site/

# Alembic setup

## Setup the migration folder using the following comment

```bash
$ alembic init -t async migrations
```

```bash
(fastapi) 3.12.4 gibson@yavar-ThinkPad-E15-Gen-2:~/Documents/gibson/learning/learn-fastapi(user-authentication-model)$ alembic init -t async migrations
  Creating directory /home/gibson/Documents/gibson/learning/learn-fastapi/migrations ...  done
  Creating directory /home/gibson/Documents/gibson/learning/learn-fastapi/migrations/versions ...  done
  Generating /home/gibson/Documents/gibson/learning/learn-fastapi/migrations/README ...  done
  Generating /home/gibson/Documents/gibson/learning/learn-fastapi/migrations/env.py ...  done
  Generating /home/gibson/Documents/gibson/learning/learn-fastapi/migrations/script.py.mako ...  done
  Generating /home/gibson/Documents/gibson/learning/learn-fastapi/alembic.ini ...  done
  Please edit configuration/connection/logging settings in /home/gibson/Documents/gibson/learning/learn-fastapi/alembic.ini before proceeding.

```

## create table

```bash
$ alembic revision --autogenerate -m "init"
```

```bash
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'users'
  Generating /home/gibson/Documents/gibson/learning/learn-fastapi/migrations/versions/a472c7a73569_init.py ...  done
```

## Apply the migration

```bash
$ alembic upgrade head
```

```bash
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> a472c7a73569, init

```

## 🧪 Common Alembic Commands (and what they do)

### Command What it does

alembic init -t async migrations ## Set up Alembic for async DBs
alembic revision --autogenerate -m "message" ##Create a migration script based on model changes
alembic upgrade head ## Apply all unapplied migrations
alembic downgrade -1 ## Undo the last migration
alembic current ## Show current DB version
alembic history ## Show all migrations (like git log)

### Redis

# three simple ways to check whether Redis is running on your system

## 🧩 Option 1 — Using the Redis CLI

```bash
$ redis-cli ping
```

✅ If Redis is running, you’ll get:

```bash
PONG
```

## ⚙️ Option 2 — Check the process (Linux / macOS)

```bash
$ ps aux | grep redis
```

✅ If Redis is running, you’ll get:

```bash
redis-server \*:6379
```

## 🪟 Option 3 — Using systemctl (Linux systems with systemd)

```bash
$ sudo systemctl status redis
```

✅ If Redis is running, you’ll get:

```bash
Active: active (running)
```

## 🧩 What “serialization” means — simple definition

Serialization means converting a Python object (like a dict, model, or class instance) into a format that can be easily stored or sent (like JSON, bytes, or text).

Deserialization is the opposite — turning that serialized format back into a Python object.
