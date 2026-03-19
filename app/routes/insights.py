from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from groq import Groq
from .. import models
from ..db import get_db
from ..auth import get_current_company
from ..config import GROQ_API_KEY

router = APIRouter(prefix="/insights", tags=["AI Insights"])
groq_client = Groq(api_key=GROQ_API_KEY)

@router.get("/")
def get_insights(
        company : models.Company = Depends(get_current_company) ,
        db : Session = Depends(get_db)
):
    total_events =  db.query(func.count(models.Event.id)).filter(models.Event.company_id == company.id).scalar()
    top_pages = db.query(models.Event.page_url,func.count(models.Event.id).label("visits")).filter(
        models.Event.company_id == company.id ,
        models.Event.event_type == "page_visits" ,
        models.Event.page_url != None
    ).group_by(models.Event.page_url).order_by(func.count(models.Event.id).desc()).limit(3).all()

    top_buttons = db.query(
        models.Event.button_id, func.count(models.Event.id).label("clicks")
    ).filter(
        models.Event.company_id == company.id,
        models.Event.event_type == "button_click",
        models.Event.button_id != None
    ).group_by(models.Event.button_id).order_by(func.count(models.Event.id).desc()).limit(3).all()

    signups = db.query(func.count(models.Event.id)).filter(
        models.Event.company_id == company.id,
        models.Event.event_type == "signup"
    ).scalar()

    suspicious_ips = db.query(
        models.Event.ip_address, func.count(models.Event.id).label("count")
    ).filter(
        models.Event.company_id == company.id,
        models.Event.event_type == "signup"
    ).group_by(models.Event.ip_address).having(func.count(models.Event.id) >= 3).all()

    prompt = f"""
    You are a senior product analyst at a top tech company. A startup has shared their user behavior data with you.
    Your job is to give them 5 sharp, specific, and actionable insights that will help them grow.

    Here is their data:
    - Total events tracked: {total_events}
    - Total signups: {signups}
    - Top pages visited: {[(p.page_url, p.visits) for p in top_pages]}
    - Top buttons clicked: {[(b.button_id, b.clicks) for b in top_buttons]}
    - Suspicious IPs (multiple signups from same IP): {[(s.ip_address, s.count) for s in suspicious_ips]}

    Rules:
    - Be direct and specific — no generic advice
    - Reference the actual data in your insights
    - If data is low, tell them exactly what to track next
    - Flag any security concerns clearly
    - Keep each insight to 2-3 sentences max
    - Format as a numbered list with a bold title for each insight
    - Tone: professional but conversational, like a smart friend who happens to be a data expert
    """

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system","content": "You are an expert product analyst who gives clear, actionable insights from user behavior data."},
            {"role": "user", "content": prompt}
        ]
    )

    return {
        "insights": response.choices[0].message.content,
        "data_summary": {
            "total_events": total_events,
            "signups": signups,
            "top_pages": [(p.page_url, p.visits) for p in top_pages],
            "top_buttons": [(b.button_id, b.clicks) for b in top_buttons],
            "suspicious_ips": len(suspicious_ips)
        }
    }