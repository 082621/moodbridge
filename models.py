from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class MoodEntry(Base):
    __tablename__ = "mood_entries"

    id = Column(Integer, primary_key=True, index=True)
    emotion = Column(String, nullable=False)          # e.g. "anxious", "happy"
    intensity = Column(Integer, nullable=False)        # 1–10
    trigger_category = Column(String, nullable=False)  # e.g. "academic", "social"
    note = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    coping_actions = relationship("CopingAction", back_populates="mood_entry", cascade="all, delete")


class CopingAction(Base):
    __tablename__ = "coping_actions"

    id = Column(Integer, primary_key=True, index=True)
    mood_entry_id = Column(Integer, ForeignKey("mood_entries.id"), nullable=False)
    action_type = Column(String, nullable=False)   # e.g. "walk", "breathing"
    helpfulness = Column(Integer, nullable=False)  # 1–5
    note = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    mood_entry = relationship("MoodEntry", back_populates="coping_actions")


class SupportResource(Base):
    __tablename__ = "support_resources"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    resource_type = Column(String, nullable=False)  # e.g. "breathing", "hotline"
    region = Column(String, nullable=False)          # "UK", "CN", "global"
    emotion_tags = Column(String, nullable=False)    # comma-separated, e.g. "anxious,stressed"
    url = Column(String, nullable=True)
    description = Column(String, nullable=False)
