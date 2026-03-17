import secrets
from datetime import datetime , timedelta
from jose import jwt , JWTError
from passlib.context import CryptContext
from fastapi import HTTPException , Depends , Header
from sqlalchemy.orm import Session
from .config import SECRET_KEY , ALGORITHM , ACCESS_TOKEN_EXPIRE_MINUTES
from .db import get_db
from . import models

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_pass(password:str) -> str:
    return pwd_context.hash(password)

def verify_pass(plain : str , hashed : str) -> bool:
    return pwd_context.verify(plain,hashed)

def generate_api_key() -> str:
    return secrets.token_hex(32)

def create_access_token(data:dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode , SECRET_KEY , algorithm=ALGORITHM)

def get_current_company(authorization : str = Header(...), db : Session = Depends(get_db)):
    try:
        scheme , token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401 , detail="Invalid auth scheme")
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        company_id = payload.get("company_id")
        if not company_id:
            raise HTTPException(status_code=401,detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401,detail="Invalid token")
    company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=401,detail="Company not found")
    return company

def get_company_by_api_key(api_key : str = Header(... , alias="X-API-Key"), db : Session = Depends(get_db)):
    company = db.query(models.Company).filter(models.Company.api_key == api_key).first()
    if not company:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return company
