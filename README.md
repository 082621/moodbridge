# MoodBridge API

A wellbeing journaling and insight REST API designed for students. Log mood entries, record coping actions, browse support resources, and explore analytics about your emotional patterns over time.

## Tech Stack

- **Python 3.11+** / **FastAPI**
- **SQLite** via SQLAlchemy ORM
- **Pydantic v2** for request/response validation
- **Swagger UI** for interactive documentation and manual testing

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
├── seed_data.py          # Populate DB with sample data
├── MoodBridge API - Swagger UI.pdf
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

This coursework submission is currently designed for reliable **local execution**.

A PDF version of the API documentation is also included in this repository:
[MoodBridge API - Swagger UI.pdf](MoodBridge%20API%20-%20Swagger%20UI.pdf)

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

## Testing Approach

Current testing is manual through Swagger UI at `/docs`. I tested each endpoint with valid and invalid payloads, including validation boundaries, missing IDs, and query filters.

The seeded 30-day sample data is used to exercise the analytics endpoints so `/summary`, `/triggers`, `/coping-effectiveness`, and `/trends` return meaningful outputs during the demo.

Automated tests are a suitable future improvement, but they are not currently included in this coursework submission.


