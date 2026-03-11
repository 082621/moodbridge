from fastapi import FastAPI
from database import Base, engine
from routers import moods, coping, resources, analytics

Base.metadata.create_all(bind=engine)

app = FastAPI(title="MoodBridge API", description="Wellbeing journaling and insight API for students")

app.include_router(moods.router)
app.include_router(coping.router)
app.include_router(resources.router)
app.include_router(analytics.router)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "MoodBridge API is running"}
