"""Populate the database with sample data for development and demo purposes."""
from datetime import datetime, timedelta
import random
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from database import SessionLocal, engine
from models import Base, MoodEntry, CopingAction, SupportResource

Base.metadata.create_all(bind=engine)

def days_ago(n: int, hour: int = 12, minute: int = 0) -> datetime:
    return datetime.utcnow() - timedelta(days=n, hours=random.randint(0, 6), minutes=random.randint(0, 59))


MOOD_ENTRIES = [
    # (days_ago, emotion, intensity, trigger_category, note)
    (1,  "anxious",  8, "academic",   "Dissertation deadline is approaching and I haven't started the analysis."),
    (2,  "stressed", 7, "academic",   "Three assignments due this week, feeling completely overwhelmed."),
    (3,  "sad",      6, "social",     "Had an argument with my flatmate, atmosphere at home is tense."),
    (4,  "angry",    7, "family",     "Parents called again asking about my grades. Felt judged and pressured."),
    (5,  "calm",     3, "health",     "Went for a long walk in the park, felt much more grounded afterward."),
    (6,  "happy",    2, "social",     "Caught up with friends over dinner, laughed a lot."),
    (7,  "anxious",  9, "financial",  "Rent is due and my student loan hasn't come through yet."),
    (8,  "stressed", 8, "academic",   "Failed a mock exam. Worried I'm not keeping up with the course."),
    (9,  "sad",      5, "social",     "Feeling isolated since moving to a new city. Miss my friends back home."),
    (10, "calm",     2, "health",     "Yoga session this morning helped clear my head."),
    (11, "angry",    6, "academic",   "Group project partner isn't contributing. Had to redo their work."),
    (12, "happy",    1, "social",     "Got positive feedback on my presentation. Felt genuinely proud."),
    (13, "anxious",  7, "health",     "Haven't been sleeping well for two weeks, starting to affect everything."),
    (14, "stressed", 6, "financial",  "Unexpected dentist bill on top of already tight budget."),
    (15, "sad",      7, "family",     "Grandparent is unwell. Feeling helpless being so far away."),
    (16, "calm",     3, "social",     "Had a quiet evening reading, felt content and at peace."),
    (17, "anxious",  8, "academic",   "Oral exam coming up. Always struggle with speaking under pressure."),
    (18, "angry",    5, "financial",  "Part-time job hours were cut without notice. Really frustrated."),
    (19, "happy",    2, "health",     "First full night of sleep in ages. Felt human again."),
    (20, "stressed", 9, "academic",   "Library closed early during exam season. Lost hours of study time."),
    (22, "sad",      6, "social",     "Wasn't invited to a flat outing. Felt left out."),
    (24, "anxious",  7, "financial",  "Scholarship application rejected. Back to worrying about fees."),
    (26, "calm",     4, "health",     "Cooked a proper meal for the first time this month. Small win."),
    (28, "happy",    3, "social",     "Joined a new campus club. Met some genuinely interesting people."),
    (30, "stressed", 7, "family",     "Family tension over holiday plans. Hard to please everyone from afar."),
]

COPING_ACTIONS = [
    # (mood_entry index 0-based, action_type, helpfulness, note)
    (0,  "breathing",      4, "Box breathing for 10 minutes before bed."),
    (0,  "journaling",     3, "Wrote out a study plan to make the deadline feel manageable."),
    (1,  "exercise",       5, "30-minute run helped burn off the stress energy."),
    (2,  "talk_to_friend", 4, "Called a friend outside the flat situation for perspective."),
    (3,  "breathing",      3, "Tried a guided meditation after the call."),
    (4,  "walk",           5, "Hour-long walk along the river. Highly recommend."),
    (6,  "journaling",     4, "Listed all expenses and made a short-term budget."),
    (7,  "talk_to_friend", 3, "Talked to a classmate who also felt behind — less alone now."),
    (8,  "walk",           4, "Walked to campus instead of taking the bus to clear my head."),
    (10, "talk_to_friend", 5, "Spoke to the module tutor about the group issue. Very helpful."),
    (12, "breathing",      4, "Sleep hygiene routine: no phone after 10pm, breathing exercises."),
    (13, "journaling",     2, "Wrote down financial worries but didn't feel much better."),
    (16, "exercise",       5, "Swam 20 laps at the sports centre before the oral."),
    (19, "walk",           3, "Short walk around the block to decompress after the library."),
    (23, "talk_to_friend", 4, "Met the new club members for coffee — made two real connections."),
]

SUPPORT_RESOURCES = [
    dict(
        title="Student Minds — UK Student Mental Health Charity",
        resource_type="campus_service",
        region="UK",
        emotion_tags="anxious,stressed,sad",
        url="https://www.studentminds.org.uk",
        description="UK charity dedicated to improving the mental health of students. Offers peer support, training, and resources.",
    ),
    dict(
        title="Samaritans Helpline",
        resource_type="hotline",
        region="UK",
        emotion_tags="sad,anxious,angry",
        url="https://www.samaritans.org",
        description="Free 24/7 helpline for anyone in emotional distress. Call 116 123 from any UK phone.",
    ),
    dict(
        title="北京心理危机研究与干预中心",
        resource_type="hotline",
        region="CN",
        emotion_tags="sad,anxious,stressed",
        url=None,
        description="24小时心理援助热线：010-82951332，提供危机干预与情绪支持服务。",
    ),
    dict(
        title="简单心理 — 在线心理咨询平台",
        resource_type="campus_service",
        region="CN",
        emotion_tags="anxious,stressed,sad",
        url="https://www.jiandanxinli.com",
        description="提供专业心理咨询预约，支持文字、语音和视频咨询，适合在校学生。",
    ),
    dict(
        title="4-7-8 Breathing Technique",
        resource_type="breathing",
        region="global",
        emotion_tags="anxious,stressed",
        url=None,
        description="Inhale for 4 seconds, hold for 7, exhale for 8. Repeat 4 cycles. Activates the parasympathetic nervous system.",
    ),
    dict(
        title="Box Breathing Exercise",
        resource_type="breathing",
        region="global",
        emotion_tags="anxious,angry,stressed",
        url=None,
        description="Inhale 4s → hold 4s → exhale 4s → hold 4s. Used by athletes and military personnel to manage acute stress.",
    ),
    dict(
        title="Understanding Student Anxiety — NHS",
        resource_type="article",
        region="UK",
        emotion_tags="anxious,stressed",
        url="https://www.nhs.uk/mental-health/feelings-symptoms-behaviours/feelings-and-symptoms/anxiety-fear-panic/",
        description="NHS guidance on recognising anxiety symptoms and practical self-help strategies.",
    ),
    dict(
        title="Crisis Text Line",
        resource_type="hotline",
        region="global",
        emotion_tags="sad,anxious,angry",
        url="https://www.crisistextline.org",
        description="Text HOME to 741741 to reach a trained crisis counsellor. Free, confidential, 24/7.",
    ),
    dict(
        title="Headspace — Meditation & Sleep App",
        resource_type="article",
        region="global",
        emotion_tags="anxious,stressed,sad",
        url="https://www.headspace.com",
        description="Guided meditation and mindfulness exercises. Free basics plan available; many universities offer free access.",
    ),
    dict(
        title="Mind — Mental Health Information",
        resource_type="article",
        region="UK",
        emotion_tags="sad,angry,stressed",
        url="https://www.mind.org.uk",
        description="Comprehensive mental health information and local support finder covering England and Wales.",
    ),
    dict(
        title="全国心理援助热线（北京）",
        resource_type="hotline",
        region="CN",
        emotion_tags="sad,stressed,anxious",
        url=None,
        description="拨打 400-161-9995 获取心理援助，由北京大学第六医院运营，免费服务。",
    ),
    dict(
        title="5-4-3-2-1 Grounding Technique",
        resource_type="breathing",
        region="global",
        emotion_tags="anxious,angry",
        url=None,
        description="Name 5 things you see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste. Anchors you to the present moment.",
    ),
]


def seed():
    db = SessionLocal()
    try:
        if db.query(MoodEntry).count() > 0:
            print("Database already has data. Skipping seed.")
            return

        # Insert mood entries
        mood_objects = []
        for days, emotion, intensity, trigger, note in MOOD_ENTRIES:
            entry = MoodEntry(
                emotion=emotion,
                intensity=intensity,
                trigger_category=trigger,
                note=note,
                created_at=days_ago(days),
            )
            db.add(entry)
            mood_objects.append(entry)

        db.flush()  # assign IDs before linking coping actions

        # Insert coping actions
        for mood_idx, action_type, helpfulness, note in COPING_ACTIONS:
            action = CopingAction(
                mood_entry_id=mood_objects[mood_idx].id,
                action_type=action_type,
                helpfulness=helpfulness,
                note=note,
                created_at=mood_objects[mood_idx].created_at + timedelta(hours=1),
            )
            db.add(action)

        # Insert support resources
        for data in SUPPORT_RESOURCES:
            db.add(SupportResource(**data))

        db.commit()
        print(f"Seeded {len(MOOD_ENTRIES)} mood entries, {len(COPING_ACTIONS)} coping actions, {len(SUPPORT_RESOURCES)} support resources.")

    except Exception as e:
        db.rollback()
        print(f"Seed failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
