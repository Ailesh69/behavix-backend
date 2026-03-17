from datetime import datetime

from sqlalchemy import String , Integer , Column , DateTime , ForeignKey , JSON
from sqlalchemy.orm import relationship
from .db import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer,primary_key=True,nullable=False)
    name = Column(String,nullable=False)
    email = Column(String,nullable=False,unique=True)
    api_key = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    created_at = Column(DateTime,default=datetime.utcnow)
    events = relationship("Event",back_populates="company")
    sessions = relationship("Sessions",back_populates="company")

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer,primary_key=True,nullable=False)
    company_id = Column(Integer,ForeignKey("companies.id"),nullable=False)
    event_type = Column(String,nullable=False)
    page_url = Column(String,nullable=True)
    button_id = Column(Integer,nullable=True)
    feature_name = Column(String,nullable=True)
    user_id = Column(String,nullable=True)
    ip_address = Column(String,nullable=True)
    event_metadata = Column(JSON,nullable=True)
    timestamp = Column(DateTime,default=datetime.utcnow)
    company = relationship("Company",back_populates="events")

class Sessions(Base):
    __tablename__ = "sessions"
    id = Column(Integer,primary_key=True,nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    user_id = Column(String, nullable=True)
    ip_address = Column(String, nullable=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    last_seen_at = Column(DateTime, default=datetime.utcnow)
    duration_seconds = Column(Integer, default=0)
    company = relationship("Company", back_populates="sessions")
