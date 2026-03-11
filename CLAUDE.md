# MoodBridge API — Project Context for Claude Code

## Project Overview
MoodBridge is a wellbeing journaling and insight REST API designed for students.
It allows users to log mood entries, record coping actions, browse support resources,
and retrieve analytics insights about their emotional patterns over time.

## Tech Stack
- **Language**: Python 3.11+
- **Framework**: FastAPI
- **Database**: SQLite (via SQLAlchemy ORM)
- **Validation**: Pydantic v2
- **Documentation**: Auto-generated Swagger UI at /docs
- **No user authentication required** (single-user demo)
- **No external AI API calls**

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
├── seed_data.py          # Script to populate DB with sample data
├── requirements.txt      # Python dependencies
└── README.md             # Setup instructions
```

## Data Models

### MoodEntry
- id (int, primary key)
- emotion (str) — e.g. "anxious", "sad", "happy", "angry", "calm", "stressed"
- intensity (int, 1–10)
- trigger_category (str) — e.g. "academic", "social", "family", "financial", "health"
- note (str, optional)
- created_at (datetime, auto)

### CopingAction (child of MoodEntry)
- id (int, primary key)
- mood_entry_id (int, foreign key → MoodEntry)
- action_type (str) — e.g. "walk", "breathing", "talk_to_friend", "journaling", "exercise"
- helpfulness (int, 1–5)
- note (str, optional)
- created_at (datetime, auto)

### SupportResource
- id (int, primary key)
- title (str)
- resource_type (str) — e.g. "breathing", "campus_service", "article", "hotline"
- region (str) — "UK", "CN", "global"
- emotion_tags (str) — comma-separated, e.g. "anxious,stressed"
- url (str, optional)
- description (str)

## API Endpoints Summary

### Mood Entries — /moods
- POST   /moods/              — create a mood entry
- GET    /moods/              — list all mood entries (supports ?emotion= and ?trigger= filters)
- GET    /moods/{id}          — get one mood entry with its coping actions
- PUT    /moods/{id}          — update a mood entry
- DELETE /moods/{id}          — delete a mood entry

### Coping Actions — /moods/{mood_id}/coping
- POST   /moods/{mood_id}/coping/       — add a coping action to a mood entry
- GET    /moods/{mood_id}/coping/       — list coping actions for a mood entry
- PUT    /moods/{mood_id}/coping/{id}   — update a coping action
- DELETE /moods/{mood_id}/coping/{id}   — delete a coping action

### Support Resources — /resources
- GET    /resources/          — list resources (supports ?emotion= and ?region= filters)
- POST   /resources/          — create a resource
- PUT    /resources/{id}      — update a resource
- DELETE /resources/{id}      — delete a resource

### Analytics — /analytics
- GET    /analytics/summary?days=7      — total entries, average intensity, emotion distribution
- GET    /analytics/triggers?days=30    — top trigger categories ranked by frequency
- GET    /analytics/coping-effectiveness — coping actions ranked by average helpfulness
- GET    /analytics/trends?days=30      — daily average intensity over time (for charts)

## Code Style Rules
- Use async def for all route handlers
- Always return appropriate HTTP status codes (201 for create, 404 for not found, 422 for validation errors)
- Use HTTPException for all error responses
- Keep each router file focused on its own resource only
- All responses must be JSON
- Add docstrings to each endpoint describing what it does

## Seed Data Requirements
seed_data.py should insert:
- At least 20 mood entries spread across the past 30 days with varied emotions and triggers
- At least 15 coping actions linked to those entries
- At least 10 support resources covering UK, CN, and global regions across different resource types

## Running the Project
```bash
pip install -r requirements.txt
python seed_data.py       # populate sample data
uvicorn main:app --reload # start dev server
# API docs available at: http://localhost:8000/docs
```

## Requirements.txt should include
fastapi
uvicorn[standard]
sqlalchemy
pydantic
python-dateutil
