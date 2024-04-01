from datetime import timedelta
from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic.networks import EmailStr
from pydantic import ValidationError
from app.schemas import IResponse, IAccount, ICreateAccount, IAuthor, IToken, Token, TokenPayload, IUserSearch
from app.models.user import User
from app.api import deps
from app import crud
from app.core.config import settings
from app.core.security import create_access_token, ALGORITHM
import secrets
from app.core.config import settings
from jose import jwt

router = APIRouter()

@router.get("/test", response_model=IResponse)
async def read_root():
  return IResponse(data=secrets.token_urlsafe(32))

@router.get("/search", response_model=IResponse)
async def list(
  req: IUserSearch = None,
  db:Session = Depends(deps.get_db),
  current_user:User = Depends(deps.get_current_user)
) -> Any:
  res = IResponse()
  res.data = crud.user.search(db)
  return res

@router.post("/search", response_model=IResponse)
async def list(
  req: IUserSearch = None,
  db:Session = Depends(deps.get_db),
  current_user:User = Depends(deps.get_current_user)
) -> Any:
  res = IResponse()
  if req.exclude:
    req.exclude = current_user.id
  res.data = crud.user.search(db, params=req)
  return res

@router.get("/id{id}", response_model=IResponse)
def get_user(
  id: int,
  db:Session = Depends(deps.get_db)
)->Any:
  """
  Get user by id.
  """
  res = IResponse()
  user = crud.user.get(db, id=id)
  if not user:
    res.setErr(110201)
  res.data = user
  return res

@router.get("/me", response_model=IResponse)
def me(
  db: Session = Depends(deps.get_db),
  current_user: User = Depends(deps.get_current_user)
)->Any:
  """
  Get current user.
  """
  res = IResponse()
  res.data = crud.user.get_full_info(db, current_user.id)
  return res

@router.post("/token-login", response_model=IResponse)
def token_login(
  background_tasks: BackgroundTasks,
  req: IToken,
  db: Session = Depends(deps.get_db)
)->Any:
  res = IResponse()
  try:
    payload = jwt.decode(
      req.token, settings.SECRET_KEY, algorithms=[ALGORITHM]
    )
    token_data = TokenPayload(**payload)
  except (jwt.JWTError, ValidationError):
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN,
      detail="Could not validate credentials",
    )
  user = crud.user.get_by_email(db, email=token_data.email)
  if not user:
    # author = crud.author.get_by_email(db=db, email=token_data.email)
    user = crud.user.create(db, obj_in = ICreateAccount(email=token_data.email, password='agist'))

  res.data = user
  return res

@router.post("/access-token", response_model=Token)
def access_token(
  db: Session = Depends(deps.get_db),
  form_data:OAuth2PasswordRequestForm = Depends()
)->Any:
  """
  user login
  """
  user = crud.user.authenticate(db, email=form_data.username, password=form_data.password)
  if not user:
    raise HTTPException(status_code=400, detail="Incorrect email or password")
  access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
  return Token(
    access_token=create_access_token(user.email, expires_delta=access_token_expires),
    token_type="bearer"
  )



@router.post("/login", response_model=IResponse)
def login(
  *,
  db: Session = Depends(deps.get_db),
  form_data:IAccount
)->Any:
  """
  user login
  """
  res = IResponse()
  user = crud.user.authenticate(db, email=form_data.email, password=form_data.password)
  if not user:
    res.setErr(110201)
    return res
  access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
  res.data = {
    "access_token": create_access_token(
      user.email, expires_delta=access_token_expires
    ),
    "token_type": "bearer",
    "user": user
  }
  return res


@router.post("/create", response_model=IResponse)
def create(
  *,
  db: Session = Depends(deps.get_db),
  user_in:ICreateAccount
)-> Any:
  """
  Create new user.
  """
  res = IResponse()
  if user_in.password != user_in.repassword:
    res.setErr(110103)
    return res
  user = crud.user.get_by_email(db, email=user_in.email)
  if user:
    res.setErr(110101)
    return res
  user_out = crud.user.create(db, obj_in=user_in)
  # if user_out.id:
  #   mail_server.sendMailToNewUser(user_out.email)
  res.data = user_out
  return res


@router.post("/email_valid", response_model=IResponse)
def email_valid(
  *,
  db: Session = Depends(deps.get_db),
  email:EmailStr = Body(None),
)-> Any:
  res = IResponse()
  user = crud.user.get_by_email(db, email=email)
  if user:
    res.setErr(110101)
  return res


@router.put("/change_password", response_model=IResponse)
def change_password(
  old_password: str = Body(None),
  new_password: str = Body(None),
  db: Session = Depends(deps.get_db),
  current_user: User = Depends(deps.get_current_user)
)-> Any:
  """
  Change user password
  """
  res = IResponse()
  verify = crud.user.authenticate(db, email=current_user.email, password=old_password)
  if not verify:
    res.setErr(110301)
    return res
  res.data = crud.user.change_password(db, id=current_user.id, password=new_password)
  return res


@router.post("/invite", response_model=IResponse)
def forgot_password(
  background_tasks: BackgroundTasks,
  email:EmailStr = Body(None),
  db: Session = Depends(deps.get_db)
)-> Any:
  """
  Invite password
  """
  res = IResponse()
  user = crud.user.get_by_email(db, email=email)
  if not user:
    res.setErr(110201)
    return res
  token = create_access_token(
    user.email,
    expires_delta=timedelta(hours=settings.EMAIL_TOKEN_EXPIRE_HOURS)
  )
  res.data = email
  # background_tasks.add_task(send_mail_invite, email=email, token=token)
  return res

@router.post("/forgot_password", response_model=IResponse)
def forgot_password(
  background_tasks: BackgroundTasks,
  email:EmailStr = Body(None),
  vcode:str = Body(None),
  db: Session = Depends(deps.get_db)
)-> Any:
  """
  Forgot password
  """
  res = IResponse()
  user = crud.user.get_by_email(db, email=email)
  if not user:
    res.setErr(110203)
    return res
  token = create_access_token(
    user.email,
    expires_delta=timedelta(hours=settings.EMAIL_TOKEN_EXPIRE_HOURS)
  )
  res.data = email
  # background_tasks.add_task(send_mail_for_reset_password, email=email, token=token)
  return res

@router.post("/user_by_token", response_model=IResponse)
def user_by_token(
  token: str = Body(None),
  db: Session = Depends(deps.get_db)
)-> Any:
  """
  Get user by token
  """
  res = IResponse()
  user = deps.get_current_user(db, token)
  if not user:
    res.setErr(110202)
    return res
  res.data = user
  return res

@router.post("/reset_password", response_model=IResponse)
def reset_password(
  background_tasks: BackgroundTasks,
  token: str = Body(None),
  new_password: str = Body(None),
  db: Session = Depends(deps.get_db)
)-> Any:
  """
  Reset password
  """
  res = IResponse()
  user = deps.get_current_user(db, token)
  if not user:
    res.setErr(110202)
    return res
  res.data = crud.user.change_password(db, id=user.id, password=new_password)
  # background_tasks.add_task(admin_send_mail_to_newuser_success, email=user.email)
  return res