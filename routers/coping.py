from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas

router = APIRouter(prefix="/moods/{mood_id}/coping", tags=["Coping Actions"])


def _get_mood_or_404(mood_id: int, db: Session) -> models.MoodEntry:
    entry = db.query(models.MoodEntry).filter(models.MoodEntry.id == mood_id).first()
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mood entry not found")
    return entry


@router.post("/", response_model=schemas.CopingActionOut, status_code=status.HTTP_201_CREATED)
async def add_coping_action(mood_id: int, payload: schemas.CopingActionCreate, db: Session = Depends(get_db)):
    """Add a coping action to a mood entry."""
    _get_mood_or_404(mood_id, db)
    action = models.CopingAction(mood_entry_id=mood_id, **payload.model_dump())
    db.add(action)
    db.commit()
    db.refresh(action)
    return action


@router.get("/", response_model=List[schemas.CopingActionOut])
async def list_coping_actions(mood_id: int, db: Session = Depends(get_db)):
    """List all coping actions for a mood entry."""
    _get_mood_or_404(mood_id, db)
    return (
        db.query(models.CopingAction)
        .filter(models.CopingAction.mood_entry_id == mood_id)
        .order_by(models.CopingAction.created_at.desc())
        .all()
    )


@router.put("/{coping_id}", response_model=schemas.CopingActionOut)
async def update_coping_action(
    mood_id: int, coping_id: int, payload: schemas.CopingActionUpdate, db: Session = Depends(get_db)
):
    """Update a coping action."""
    _get_mood_or_404(mood_id, db)
    action = (
        db.query(models.CopingAction)
        .filter(models.CopingAction.id == coping_id, models.CopingAction.mood_entry_id == mood_id)
        .first()
    )
    if not action:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coping action not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(action, field, value)
    db.commit()
    db.refresh(action)
    return action


@router.delete("/{coping_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_coping_action(mood_id: int, coping_id: int, db: Session = Depends(get_db)):
    """Delete a coping action."""
    _get_mood_or_404(mood_id, db)
    action = (
        db.query(models.CopingAction)
        .filter(models.CopingAction.id == coping_id, models.CopingAction.mood_entry_id == mood_id)
        .first()
    )
    if not action:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coping action not found")
    db.delete(action)
    db.commit()
