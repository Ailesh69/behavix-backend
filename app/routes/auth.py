from fastapi import APIRouter , Depends , HTTPException
from sqlalchemy.orm import Session
from .. import schemas , crud
from ..db import get_db
from ..auth import verify_pass , create_access_token

router = APIRouter(prefix="/auth",tags=["Authentication"])

@router.post("/register",response_model=schemas.CompanyResponse)
def register(data : schemas.CompanyRegister , db : Session = Depends(get_db)):
    if crud.get_company_by_email(db , data.email):
        raise HTTPException(status_code=400 , detail="Email already registered ")
    return crud.create_company(db ,data)

@router.post("/login", response_model=schemas.Token)
def login(data : schemas.CompanyLogin , db : Session = Depends(get_db)):
    company = crud.get_company_by_email(db , data.email)
    if not company or not verify_pass(data.password , company.password):
        raise HTTPException(status_code=401 , detail="Invalid email or password")
    token = create_access_token({"company_id":company.id})
    return {"access_token":token,"token_type":"bearer"}
