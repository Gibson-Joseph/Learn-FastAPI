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

# 🔴 Redis – In-Memory Data Store

Redis (Remote Dictionary Server) is an open-source, in-memory data structure store used as a database, cache, and message broker.
It’s extremely fast because it keeps data in memory instead of disk, making it ideal for high-performance backend systems.

## three simple ways to check whether Redis is running on your system

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

# 🐝 Celery – Asynchronous Task Queue

Celery is an asynchronous task queue or job queue that’s widely used in Python backend development for running background tasks outside the main request–response cycle — making your app faster and more scalable.

Celery is a distributed task queue that allows you to execute time-consuming or scheduled jobs asynchronously.
It means instead of making the user wait while your app completes a long operation, you can offload that work to Celery to be executed in the background.

# ⚙️ Typical Use Cases

Sending emails in the background.
Generating reports or processing large files.
Calling external APIs without blocking the main thread.
Scheduling periodic tasks (like CRON jobs).
Running machine learning or data processing jobs asynchronously.

## Install Celery

```bash
$ pip install celery
```

## Start a Worker

```bash
$ celery -A src.celery_tasks.c_app worker --loglevel=info
```

## Workers are background executors that continuously “listen” to the Redis broker for new jobs.

```bash
          ┌──────────────────┐
          │  FastAPI Server  │
          │ (main process)   │
          └──────┬───────────┘
                 │ Adds task to queue
                 ▼
          ┌──────────────────┐
          │   Redis Broker   │
          │ (task queue)     │
          └──────┬───────────┘
                 │
     ┌───────────┴───────────┐
     │                       │
┌────────────┐         ┌────────────┐
│ Celery     │         │ Celery     │
│ Worker #1  │         │ Worker #2  │
└────────────┘         └────────────┘
     │                       │
     ▼                       ▼
 Executes task         Executes another task
```

## 🧩 How you start workers

You start them from the command line:

```bash
celery -A src.celery_tasks.c_app worker --loglevel=info
```

This starts a background process that:

1. Connects to your broker (e.g., Redis)
2. Listens for new messages (tasks)
3. Executes them when available

You can run multiple workers — even on different servers — and they’ll all pull tasks from the same queue.

| Term                 | Meaning                                             |
| -------------------- | --------------------------------------------------- |
| **Worker**           | A background process that executes Celery tasks     |
| **Broker**           | The message queue that holds tasks (Redis/RabbitMQ) |
| **Backend**          | Optional store for task results/status              |
| **Multiple Workers** | Allow parallel and distributed processing           |

# 🌼 What is Flower?

Flower is a real-time web-based monitoring tool for Celery.
It lets you visually track and manage your Celery workers, tasks, and queues through a dashboard.

In short:

🧠 Flower = Celery’s monitoring dashboard.

## 🔍 Why you need it

When Celery is running, tasks are distributed among multiple workers, possibly across servers.
Tracking their:

1. status,
2. progress,
3. failures,
4. or retries

can get difficult using just logs.

✅ Flower gives you a live web interface to monitor all that.

## 🧩 Installation

```bash
$ pip install flower
```

## 🚀 How to start Flower

```bash
celery -A src.celery_tasks.c_app flower
```

Open http://localhost:5555

## Monitoring with celery events

Celery also comes with a real-time event console — basically a text-based version of Flower.

```bash
celery -A src.celery_tasks.c_app events
```
