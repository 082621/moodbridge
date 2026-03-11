from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas

router = APIRouter(prefix="/moods", tags=["Moods"])


@router.post("/", response_model=schemas.MoodEntryOut, status_code=status.HTTP_201_CREATED)
async def create_mood_entry(payload: schemas.MoodEntryCreate, db: Session = Depends(get_db)):
    """Create a new mood entry."""
    entry = models.MoodEntry(**payload.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.get("/", response_model=List[schemas.MoodEntryOut])
async def list_mood_entries(
    emotion: Optional[str] = None,
    trigger: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """List all mood entries, optionally filtered by emotion or trigger category."""
    query = db.query(models.MoodEntry)
    if emotion:
        query = query.filter(models.MoodEntry.emotion == emotion)
    if trigger:
        query = query.filter(models.MoodEntry.trigger_category == trigger)
    return query.order_by(models.MoodEntry.created_at.desc()).all()


@router.get("/{mood_id}", response_model=schemas.MoodEntryOut)
async def get_mood_entry(mood_id: int, db: Session = Depends(get_db)):
    """Get a single mood entry including its coping actions."""
    entry = db.query(models.MoodEntry).filter(models.MoodEntry.id == mood_id).first()
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mood entry not found")
    return entry


@router.put("/{mood_id}", response_model=schemas.MoodEntryOut)
async def update_mood_entry(mood_id: int, payload: schemas.MoodEntryUpdate, db: Session = Depends(get_db)):
    """Update an existing mood entry."""
    entry = db.query(models.MoodEntry).filter(models.MoodEntry.id == mood_id).first()
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mood entry not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(entry, field, value)
    db.commit()
    db.refresh(entry)
    return entry


@router.delete("/{mood_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_mood_entry(mood_id: int, db: Session = Depends(get_db)):
    """Delete a mood entry and its associated coping actions."""
    entry = db.query(models.MoodEntry).filter(models.MoodEntry.id == mood_id).first()
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mood entry not found")
    db.delete(entry)
    db.commit()
