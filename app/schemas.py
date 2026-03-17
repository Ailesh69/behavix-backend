from pydantic import BaseModel , ConfigDict , EmailStr , field_validator
from typing import Optional, Any
from datetime import datetime
import re

#company schema
class CompanyRegister(BaseModel):
    name : str
    email : EmailStr
    password : str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8 :
            raise ValueError("Password must be greater than 8 characters")
        if not re.search(r"\d",v):
            raise ValueError("Password must contain at least one number")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must have at least one special character")
        return v

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError("Company name cannot be empty")
        return v.strip()

class CompanyLogin(BaseModel):
    email: EmailStr
    password: str

class CompanyResponse(BaseModel):
    id: int
    name: str
    email: str
    api_key: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

#Event schema
class EventCreate(BaseModel):
    event_type: str
    page_url: Optional[str] = None
    button_id: Optional[str] = None
    feature_name: Optional[str] = None
    user_id: Optional[str] = None
    ip_address: Optional[str] = None
    metadata: Optional[Any] = None

    @field_validator("event_type")
    @classmethod
    def validate_event_type(cls, v):
        allowed = ["page_visit", "button_click", "signup", "feature_usage"]
        if v not in allowed:
            raise ValueError(f"event_type must be one of {allowed}")
        return v

class EventResponse(BaseModel):
    id: int
    event_type: str
    page_url: Optional[str]
    button_id: Optional[str]
    feature_name: Optional[str]
    user_id: Optional[str]
    ip_address: Optional[str]
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)
