# MoodBridge API

A wellbeing journaling and insight REST API designed for students. Log mood entries, record coping actions, browse support resources, and explore analytics about your emotional patterns over time.

## Tech Stack

- **Python 3.11+** / **FastAPI**
- **SQLite** via SQLAlchemy ORM
- **Pydantic v2** for request/response validation
- **pytest + httpx** for async testing

## Project Structure

```
moodbridge/
├── main.py               # App entry point, mounts all routers
├── database.py           # SQLite connection and session setup
├── models.py             # SQLAlchemy table definitions
├── schemas.py            # Pydantic request/response schemas
├── routers/
│   ├── moods.py          # Mood entry CRUD endpoints
│   ├── coping.py         # Coping action CRUD endpoints
│   ├── resources.py      # Support resources endpoints
│   └── analytics.py      # Analytics and insights endpoints
├── tests/
│   ├── conftest.py       # Shared fixtures (test DB, async client)
│   ├── test_moods.py
│   ├── test_coping.py
│   ├── test_resources.py
│   └── test_analytics.py
├── seed_data.py          # Populate DB with sample data
└── requirements.txt
```

## Getting Started

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Seed sample data

```bash
python seed_data.py
```

This inserts 20+ mood entries, 15+ coping actions, and 10+ support resources into `moodbridge.db`.

### 3. Start the server

```bash
uvicorn main:app --reload
```

After running the server locally, interactive API docs are available at:
http://localhost:8000/docs

A PDF version of the API documentation is also included in this repository:
[MoodBridge API - Swagger UI.pdf]

## API Overview

### Mood Entries — `/moods`

| Method | Path | Description |
|--------|------|-------------|
| POST | `/moods/` | Create a mood entry |
| GET | `/moods/` | List all entries (filter by `?emotion=` or `?trigger=`) |
| GET | `/moods/{id}` | Get one entry with its coping actions |
| PUT | `/moods/{id}` | Update a mood entry |
| DELETE | `/moods/{id}` | Delete a mood entry |

### Coping Actions — `/moods/{mood_id}/coping`

| Method | Path | Description |
|--------|------|-------------|
| POST | `/moods/{mood_id}/coping/` | Add a coping action |
| GET | `/moods/{mood_id}/coping/` | List coping actions for an entry |
| PUT | `/moods/{mood_id}/coping/{id}` | Update a coping action |
| DELETE | `/moods/{mood_id}/coping/{id}` | Delete a coping action |

### Support Resources — `/resources`

| Method | Path | Description |
|--------|------|-------------|
| GET | `/resources/` | List resources (filter by `?region=` or `?emotion=`) |
| POST | `/resources/` | Create a resource |
| PUT | `/resources/{id}` | Update a resource |
| DELETE | `/resources/{id}` | Delete a resource |

### Analytics — `/analytics`

| Method | Path | Description |
|--------|------|-------------|
| GET | `/analytics/summary?days=7` | Total entries, average intensity, emotion distribution |
| GET | `/analytics/triggers?days=30` | Top trigger categories by frequency |
| GET | `/analytics/coping-effectiveness` | Coping actions ranked by average helpfulness |
| GET | `/analytics/trends?days=30` | Daily average intensity (for charts) |

## Data Models

### MoodEntry
| Field | Type | Notes |
|-------|------|-------|
| `emotion` | string | e.g. `anxious`, `happy`, `sad`, `calm`, `stressed` |
| `intensity` | int (1–10) | Severity of the emotion |
| `trigger_category` | string | e.g. `academic`, `social`, `financial`, `health` |
| `note` | string (optional) | Free-text note |

### CopingAction
| Field | Type | Notes |
|-------|------|-------|
| `action_type` | string | e.g. `walk`, `breathing`, `journaling`, `exercise` |
| `helpfulness` | int (1–5) | How helpful the action was |
| `note` | string (optional) | Free-text note |

### SupportResource
| Field | Type | Notes |
|-------|------|-------|
| `title` | string | Resource name |
| `resource_type` | string | e.g. `breathing`, `hotline`, `article`, `campus_service` |
| `region` | string | `UK`, `CN`, or `global` |
| `emotion_tags` | string | Comma-separated, e.g. `anxious,stressed` |
| `url` | string (optional) | Link to the resource |
| `description` | string | Short description |

## Running Tests

Tests use an isolated SQLite database and never touch `moodbridge.db`.

```bash
pytest tests/ -v
```

25 tests covering all endpoints — CRUD, validation boundaries, filters, and analytics.
