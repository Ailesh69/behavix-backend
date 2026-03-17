from sqlalchemy.orm import Session
from . import models, schemas
from .auth import hash_pass, generate_api_key


# Company Crud
def create_company(db: Session, data: schemas.CompanyRegister) -> models.Company:
    company = models.Company(
        name=data.name,
        email=data.email,
        password=hash_pass(data.password),
        api_key=generate_api_key()
    )
    db.add(company)
    db.commit()
    db.refresh(company)
    return company

def get_company_by_email(db: Session, email: str):
    return db.query(models.Company).filter(models.Company.email == email).first()

def regenerate_api_key(db: Session, company: models.Company) -> models.Company:
    company.api_key = generate_api_key()
    db.commit()
    db.refresh(company)
    return company

# Event crud
def create_event(db: Session, data: schemas.EventCreate, company_id: int) -> models.Event:
    event = models.Event(
        company_id=company_id,
        event_type=data.event_type,
        page_url=data.page_url,
        button_id=data.button_id,
        feature_name=data.feature_name,
        user_id=data.user_id,
        ip_address=data.ip_address,
        event_metadata=data.metadata
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

def get_events(db: Session, company_id: int, skip: int = 0, limit: int = 20,
               event_type: str = None):
    query = db.query(models.Event).filter(models.Event.company_id == company_id)
    if event_type:
        query = query.filter(models.Event.event_type == event_type)
    return query.order_by(models.Event.timestamp.desc()).offset(skip).limit(limit).all()