from fastapi import APIRouter, Depends
from .. import schemas, models
from ..auth import get_current_company
from ..crud import regenerate_api_key
from ..db import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/company", tags=["Company"])


@router.get("/me", response_model=schemas.CompanyResponse)
def get_my_company(company: models.Company = Depends(get_current_company)):
    return company


@router.post("/regenerate-key", response_model=schemas.CompanyResponse)
def regenerate_key(
    company: models.Company = Depends(get_current_company),
    db: Session = Depends(get_db)
):
    return regenerate_api_key(db, company)