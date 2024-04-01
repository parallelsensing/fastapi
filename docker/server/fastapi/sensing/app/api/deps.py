from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from sqlalchemy.orm import Session
from jose import jwt
from datetime import datetime, timedelta
from app.db.session import SessionLocal
from app.models import User
from app.schemas import  TokenPayload
from app.core import security
from app import crud
from app.core.config import settings
from openai import OpenAI
import httpx
import json


reusable_oauth2 = OAuth2PasswordBearer(
  tokenUrl=f"{settings.API_PATH}/user/access-token"
)

def get_db() -> Generator:
  try:
    db = SessionLocal()
    yield db
  finally:
    db.close()

def get_current_user(
  db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> User:
  try:
    payload = jwt.decode(
      token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
    )
    token_data = TokenPayload(**payload)
  except (jwt.JWTError, ValidationError):
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN,
      detail="Could not validate credentials",
    )
  user = crud.user.get_by_email(db, email=token_data.email)
  if not user:
    raise HTTPException(status_code=404, detail="User not found")
  return user

