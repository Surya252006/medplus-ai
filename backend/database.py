import sqlite3
import os
import uuid
import json
from datetime import datetime
from typing import List, Optional, Dict, Any

DB_FILE = os.path.join(os.path.dirname(__file__), "..", "medpulse.db")

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assessments (
            id TEXT PRIMARY KEY,
            created_at TEXT NOT NULL,
            symptoms_original TEXT NOT NULL,
            language TEXT NOT NULL,
            age_group TEXT,
            duration TEXT,
            urgency_category TEXT NOT NULL,
            urgency_color TEXT NOT NULL,
            recommended_facility_type TEXT NOT NULL,
            summary_text TEXT NOT NULL,
            clinician_acknowledged INTEGER DEFAULT 0,
            clinician_notes TEXT DEFAULT ''
        )
    """)
    conn.commit()
    conn.close()

def save_assessment(
    symptoms_original: str,
    language: str,
    age_group: str,
    duration: str,
    urgency_category: str,
    urgency_color: str,
    recommended_facility_type: str,
    summary_text: str
) -> str:
    conn = get_db_connection()
    cursor = conn.cursor()
    record_id = f"MP-{uuid.uuid4().hex[:8].upper()}"
    now_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    cursor.execute("""
        INSERT INTO assessments (
            id, created_at, symptoms_original, language, age_group, duration,
            urgency_category, urgency_color, recommended_facility_type, summary_text,
            clinician_acknowledged, clinician_notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, '')
    """, (
        record_id, now_str, symptoms_original, language, age_group, duration,
        urgency_category, urgency_color, recommended_facility_type, summary_text
    ))
    conn.commit()
    conn.close()
    return record_id

def get_assessments(limit: int = 50) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM assessments ORDER BY created_at DESC LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    
    results = []
    for row in rows:
        results.append({
            "id": row["id"],
            "created_at": row["created_at"],
            "symptoms_original": row["symptoms_original"],
            "language": row["language"],
            "age_group": row["age_group"],
            "duration": row["duration"],
            "urgency_category": row["urgency_category"],
            "urgency_color": row["urgency_color"],
            "recommended_facility_type": row["recommended_facility_type"],
            "summary_text": row["summary_text"],
            "clinician_acknowledged": bool(row["clinician_acknowledged"]),
            "clinician_notes": row["clinician_notes"] or ""
        })
    return results

def get_assessment_by_id(assessment_id: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM assessments WHERE id = ?", (assessment_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    return {
        "id": row["id"],
        "created_at": row["created_at"],
        "symptoms_original": row["symptoms_original"],
        "language": row["language"],
        "age_group": row["age_group"],
        "duration": row["duration"],
        "urgency_category": row["urgency_category"],
        "urgency_color": row["urgency_color"],
        "recommended_facility_type": row["recommended_facility_type"],
        "summary_text": row["summary_text"],
        "clinician_acknowledged": bool(row["clinician_acknowledged"]),
        "clinician_notes": row["clinician_notes"] or ""
    }

def delete_assessment(assessment_id: str) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM assessments WHERE id = ?", (assessment_id,))
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0

def delete_all_assessments() -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM assessments")
    count = cursor.rowcount
    conn.commit()
    conn.close()
    return count

def acknowledge_assessment(assessment_id: str, clinician_notes: str) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE assessments 
        SET clinician_acknowledged = 1, clinician_notes = ? 
        WHERE id = ?
    """, (clinician_notes, assessment_id))
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0

# Seed with 3 realistic synthetic demonstration cases for hackathon preview
def seed_demo_assessments():
    existing = get_assessments(limit=1)
    if existing:
        return
    
    demo_cases = [
        (
            "நெஞ்சு வலி, இடது கை வலி மற்றும் அதிக வியர்வை",
            "ta",
            "adult",
            "< 24 hours",
            "EMERGENCY",
            "#EF4444",
            "Taluk Hospital or Tertiary Care Center",
            "Patient reports acute severe chest pain radiating to the left arm with profuse diaphoresis. Critical cardiac red flag detected. Advised immediate 108 emergency transport."
        ),
        (
            "High fever for 4 days, severe body aches, rash on legs, unable to eat",
            "en",
            "adult",
            "4-7 days",
            "URGENT",
            "#F59E0B",
            "Community Health Centre (CHC)",
            "Prolonged high fever with rash and poor oral intake. Suspected acute febrile illness (Dengue/Chikungunya workup indicated). Recommended urgent medical evaluation within 12 hours."
        ),
        (
            "हल्की खांसी और नाक बहना, गले में खराश दो दिन से",
            "hi",
            "child",
            "1-3 days",
            "ROUTINE",
            "#10B981",
            "Primary Health Centre (PHC) / Sub-Centre",
            "Upper respiratory tract viral symptoms without respiratory distress. Suitable for local Primary Health Centre outpatient consultation and supportive home hydration."
        )
    ]
    for case in demo_cases:
        save_assessment(*case)
