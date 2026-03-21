from fastapi import APIRouter , Depends
from sqlalchemy.orm import Session
from ..db import get_db
from sqlalchemy import func
from datetime import datetime , timedelta
from .. import  models
from ..auth import get_current_company

router = APIRouter(prefix="/analytics",tags=["Analytics"])

@router.get("/overview")
def get_overview(
        company : models.Company = Depends(get_current_company),
        db : Session = Depends(get_db)
):
    total_events = db.query(func.count(models.Event.id)).filter(models.Event.company_id == company.id).scalar()
    page_visits = db.query(func.count(models.Event.id)).filter(models.Event.company_id == company.id , models.Event.event_type == "page_visit").scalar()
    signups = db.query(func.count(models.Event.id)).filter(
        models.Event.company_id == company.id,
        models.Event.event_type == "signup"
    ).scalar()

    active_users = db.query(func.count(func.distinct(models.Event.user_id))).filter(
        models.Event.company_id == company.id,
        models.Event.timestamp >= datetime.utcnow() - timedelta(days=30)
    ).scalar()
    return {
        "total_events": total_events,
        "page_visits": page_visits,
        "signups": signups,
        "active_users": active_users
    }

@router.get("/pages")
def get_top_pages(company : models.Company = Depends(get_current_company),
                  db : Session = Depends(get_db)):
    results = db.query(models.Event.page_url,func.count(models.Event.id).label("visits")).filter(
        models.Event.company_id == company.id ,
        models.Event.event_type == "page_visit",
        models.Event.page_url != None
    ).group_by(models.Event.page_url).order_by(func.count(models.Event.id).desc()).limit(5).all()
    return [{"page_url":r.page_url , "visits":r.visits} for r in results]

@router.get("/buttons")
def get_top_buttons(
    company: models.Company = Depends(get_current_company),
    db: Session = Depends(get_db)
):
    results = db.query(
        models.Event.button_id,
        func.count(models.Event.id).label("clicks")
    ).filter(
        models.Event.company_id == company.id,
        models.Event.event_type == "button_click",
        models.Event.button_id != None
    ).group_by(models.Event.button_id).order_by(func.count(models.Event.id).desc()).limit(5).all()

    return [{"button_id": r.button_id, "clicks": r.clicks} for r in results]

@router.get("/features")
def get_feature_usage(
    company: models.Company = Depends(get_current_company),
    db: Session = Depends(get_db)
):
    results = db.query(
        models.Event.feature_name,
        func.count(models.Event.id).label("usage_count")
    ).filter(
        models.Event.company_id == company.id,
        models.Event.event_type == "feature_usage",
        models.Event.feature_name != None
    ).group_by(models.Event.feature_name).order_by(func.count(models.Event.id).desc()).all()

    return [{"feature_name": r.feature_name, "usage_count": r.usage_count} for r in results]

@router.get("/suspicious-ips")
def get_suspicious_ips(
    company: models.Company = Depends(get_current_company),
    db: Session = Depends(get_db)
):
    results = db.query(
        models.Event.ip_address,
        func.count(models.Event.id).label("signup_count")
    ).filter(
        models.Event.company_id == company.id,
        models.Event.event_type == "signup",
        models.Event.ip_address != None
    ).group_by(models.Event.ip_address).having(
        func.count(models.Event.id) >= 3
    ).order_by(func.count(models.Event.id).desc()).all()

    return [{"ip_address": r.ip_address, "signup_count": r.signup_count} for r in results]

@router.get("/trends")
def get_trends(
    company: models.Company = Depends(get_current_company),
    db: Session = Depends(get_db)
):
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    results = db.query(
        func.date(models.Event.timestamp).label("date"),
        func.count(models.Event.id).label("count")
    ).filter(
        models.Event.company_id == company.id,
        models.Event.timestamp >= thirty_days_ago
    ).group_by(func.date(models.Event.timestamp)).order_by("date").all()

    return [{"date": str(r.date), "count": r.count} for r in results]