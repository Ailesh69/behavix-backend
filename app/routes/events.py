from fastapi import APIRouter , Depends
from sqlalchemy.orm import Session
from ..db import get_db
from typing import Optional, List
from .. import schemas , models , crud
from ..auth import get_current_company , get_company_by_api_key

router = APIRouter(tags=["Events"])

@router.post("/events",response_model=schemas.EventResponse)
def ingest_event(
        data : schemas.EventCreate ,
        company : models.Company = Depends(get_company_by_api_key) ,
        db : Session = Depends(get_db)
):
    return crud.create_event(db,data,company.id)

@router.get("/events",response_model=List[schemas.EventResponse])
def get_events(
        skip : int = 0 ,
        limit : int = 20 ,
        event_type : Optional[str] = None ,
        company : models.Company = Depends(get_current_company) ,
        db : Session = Depends(get_db)
):
    return crud.get_events(db , company.id , skip , limit , event_type)