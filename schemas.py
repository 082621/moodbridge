from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


# ── CopingAction ─────────────────────────────────────────────────────────────

class CopingActionCreate(BaseModel):
    action_type: str
    helpfulness: int = Field(..., ge=1, le=5)
    note: Optional[str] = None


class CopingActionUpdate(BaseModel):
    action_type: Optional[str] = None
    helpfulness: Optional[int] = Field(None, ge=1, le=5)
    note: Optional[str] = None


class CopingActionOut(BaseModel):
    id: int
    mood_entry_id: int
    action_type: str
    helpfulness: int
    note: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}


# ── MoodEntry ─────────────────────────────────────────────────────────────────

class MoodEntryCreate(BaseModel):
    emotion: str
    intensity: int = Field(..., ge=1, le=10)
    trigger_category: str
    note: Optional[str] = None


class MoodEntryUpdate(BaseModel):
    emotion: Optional[str] = None
    intensity: Optional[int] = Field(None, ge=1, le=10)
    trigger_category: Optional[str] = None
    note: Optional[str] = None


class MoodEntryOut(BaseModel):
    id: int
    emotion: str
    intensity: int
    trigger_category: str
    note: Optional[str]
    created_at: datetime
    coping_actions: List[CopingActionOut] = []

    model_config = {"from_attributes": True}


# ── SupportResource ───────────────────────────────────────────────────────────

class SupportResourceCreate(BaseModel):
    title: str
    resource_type: str
    region: str
    emotion_tags: str
    url: Optional[str] = None
    description: str


class SupportResourceUpdate(BaseModel):
    title: Optional[str] = None
    resource_type: Optional[str] = None
    region: Optional[str] = None
    emotion_tags: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None


class SupportResourceOut(BaseModel):
    id: int
    title: str
    resource_type: str
    region: str
    emotion_tags: str
    url: Optional[str]
    description: str

    model_config = {"from_attributes": True}


# ── Analytics ─────────────────────────────────────────────────────────────────

class SummaryOut(BaseModel):
    total_entries: int
    average_intensity: float
    emotion_distribution: dict


class TriggerFrequencyOut(BaseModel):
    trigger_category: str
    count: int


class CopingEffectivenessOut(BaseModel):
    action_type: str
    average_helpfulness: float


class TrendPointOut(BaseModel):
    date: str
    average_intensity: float
