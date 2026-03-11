from collections import defaultdict
from datetime import datetime, timedelta, timezone
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas

router = APIRouter(prefix="/analytics", tags=["Analytics"])


def _since(days: int) -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=days)


@router.get("/summary", response_model=schemas.SummaryOut)
async def get_summary(days: int = 7, db: Session = Depends(get_db)):
    """Return total entries, average intensity, and emotion distribution for the past N days."""
    entries = (
        db.query(models.MoodEntry)
        .filter(models.MoodEntry.created_at >= _since(days))
        .all()
    )
    total = len(entries)
    avg_intensity = round(sum(e.intensity for e in entries) / total, 2) if total else 0.0
    distribution: dict = defaultdict(int)
    for e in entries:
        distribution[e.emotion] += 1
    return schemas.SummaryOut(
        total_entries=total,
        average_intensity=avg_intensity,
        emotion_distribution=dict(distribution),
    )


@router.get("/triggers", response_model=List[schemas.TriggerFrequencyOut])
async def get_top_triggers(days: int = 30, db: Session = Depends(get_db)):
    """Return top trigger categories ranked by frequency over the past N days."""
    rows = (
        db.query(models.MoodEntry.trigger_category, func.count(models.MoodEntry.id).label("count"))
        .filter(models.MoodEntry.created_at >= _since(days))
        .group_by(models.MoodEntry.trigger_category)
        .order_by(func.count(models.MoodEntry.id).desc())
        .all()
    )
    return [schemas.TriggerFrequencyOut(trigger_category=r.trigger_category, count=r.count) for r in rows]


@router.get("/coping-effectiveness", response_model=List[schemas.CopingEffectivenessOut])
async def get_coping_effectiveness(db: Session = Depends(get_db)):
    """Return coping action types ranked by average helpfulness score."""
    rows = (
        db.query(
            models.CopingAction.action_type,
            func.avg(models.CopingAction.helpfulness).label("avg_help"),
        )
        .group_by(models.CopingAction.action_type)
        .order_by(func.avg(models.CopingAction.helpfulness).desc())
        .all()
    )
    return [
        schemas.CopingEffectivenessOut(action_type=r.action_type, average_helpfulness=round(r.avg_help, 2))
        for r in rows
    ]


@router.get("/trends", response_model=List[schemas.TrendPointOut])
async def get_trends(days: int = 30, db: Session = Depends(get_db)):
    """Return daily average intensity over the past N days, suitable for charting."""
    entries = (
        db.query(models.MoodEntry)
        .filter(models.MoodEntry.created_at >= _since(days))
        .all()
    )
    daily: dict = defaultdict(list)
    for e in entries:
        day = e.created_at.strftime("%Y-%m-%d")
        daily[day].append(e.intensity)
    return [
        schemas.TrendPointOut(date=day, average_intensity=round(sum(vals) / len(vals), 2))
        for day, vals in sorted(daily.items())
    ]
