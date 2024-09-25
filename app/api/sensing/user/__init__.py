from fastapi import FastAPI, Depends, HTTPException, APIRouter,BackgroundTasks
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.schemas import LoginRequest, LoginResponse, UserInfo, UserCreate, UserResponse,UserForgotPasswordRequest,UserResetPasswordRequest,EmailForGetPasswordRequest
from app.models import User as UserModel
from typing import List
from app.core.token import create_token, verify_token, get_current_user
from app.core.security import hash_password,verify_password
from app.utils import is_valid_email,send_email
from app.core.captcha.captcha import Captcha
# app = FastAPI()
import asyncio

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# 获取注册验证码
@router.post("/get_create_code",response_model=UserResponse)
async def get_create_code(email:EmailForGetPasswordRequest,background_tasks:BackgroundTasks, db: Session = Depends(get_db))->UserResponse:
    if not is_valid_email(email.email):
        return UserResponse(code=400, msg="Invalid email address")
    
    user = db.query(UserModel).filter(UserModel.email == email.email).first()
    
    if user:
        return UserResponse(code=400, msg="User already registered")
    
    captcha = Captcha().generate_captcha(email.email)
    if not captcha:
        return UserResponse(code=400, msg="captcha have been sent")
    background_tasks.add_task(send_email, "register", email.email, captcha.code, 1) 

    return UserResponse(code=200,msg='success')


@router.post("/create", response_model=UserResponse)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    if not is_valid_email(user_data.email):
        return UserResponse(code=400, msg="Invalid email address")
    
    caseptcha = Captcha()
    if not caseptcha.check_captcha(user_data.email,user_data.code):
        raise HTTPException(status_code=401, detail="Incorrect captcha")
    del caseptcha
    
    db_user = db.query(UserModel).filter(UserModel.email == user_data.email).first()
    if db_user:
        return UserResponse(code=400, msg="User already registered")
    hashed_password = hash_password(user_data.password)
    print(hashed_password)

    new_user = UserModel(
        username=user_data.username,
        nickname=user_data.nickname,
        password=hashed_password,
        email=user_data.email
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # 成功创建用户，构造响应
    return UserResponse(code=200, data=new_user.to_json(), msg="User created successfully")


@router.post("/login", response_model=LoginResponse)
def login(login_request: LoginRequest, db: Session = Depends(get_db)) -> LoginResponse:
    if not is_valid_email(login_request.email):
        return LoginResponse(code=400, msg="Invalid email address", data={})
    user = db.query(UserModel).filter(UserModel.email == login_request.email).first()
    
    if not user:
        return LoginResponse(code=404, msg="User not found", data={})

    if not verify_password(user.password,login_request.password):
        return LoginResponse(code=401, msg="Incorrect password", data={})
    
    token = create_token(user.username)

    # return LoginResponse(code=200, msg="Login successful", data={"token": token,"data":user.to_json()})
    return LoginResponse(code=200, msg="Login successful", data=user.to_json(),token=token)
@router.post("/change_password",response_model=UserResponse)
def change_password(resetBody:UserResetPasswordRequest, db: Session = Depends(get_db)):
    if not is_valid_email(resetBody.email):
        return UserResponse(code=400, msg="Invalid email address")
    email:str = resetBody.email
        
    old_password:str = resetBody.old_password
    new_password:str = resetBody.new_password
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    old_hashed_password = hash_password(old_password)
    if user.password != old_hashed_password:
        raise HTTPException(status_code=401, detail="Incorrect password")
    
    hashed_password = hash_password(new_password)
    user.password = hashed_password
    
    db.commit()
    db.refresh(user)
    return UserResponse(code=200, data=None, msg="Password reset successful")

@router.post("/forgot_password", response_model=UserResponse)
async def forgot_password(emailForGetPasswordRequest: EmailForGetPasswordRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db) ):
    if not is_valid_email(emailForGetPasswordRequest.email):
        return UserResponse(code=400, msg="Invalid email address")
    
    email: str = emailForGetPasswordRequest.email
    caseptcha = Captcha()
    captcha = caseptcha.generate_captcha(email)
    del caseptcha 
    
    if not captcha:
        return UserResponse(code=400, msg="captcha have been sent")
     
    # 将 send_email 添加到后台任务中
    background_tasks.add_task(send_email, "reset_password", email, captcha.code, 1)
    
    return UserResponse(code=200, data=None, msg="Send email successful")

@router.post("/reset_password",response_model=UserResponse)
def reset_password(forgotBody:UserForgotPasswordRequest, db: Session = Depends(get_db)):
    if not is_valid_email(forgotBody.email):
        return UserResponse(code=400, msg="Invalid email address")
    
    email:str = forgotBody.email
    code:str = forgotBody.code
    
    caseptcha = Captcha()
    if not caseptcha.check_captcha(email,code):
        raise HTTPException(status_code=401, detail="Incorrect captcha")
    del caseptcha
    
    new_password:str = forgotBody.new_password
    hashed_password = hash_password(new_password)

    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.password = hashed_password
    db.commit()
    db.refresh(user)
    
    return UserResponse(code=200, data=None, msg="Password reset successful")

@router.get("/get_users/{username}", response_model=UserInfo)
def get_user(username: str, db: Session = Depends(get_db), token: str = Depends(get_current_user)) -> UserInfo:
    user = db.query(UserModel).filter(UserModel.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user  # 这里直接返回数据库模型实例

# return all users
@router.get("/get_users", response_model=List[UserInfo])
def get_all_users(db: Session = Depends(get_db), username: str = Depends(get_current_user)) -> List[UserInfo]:
    users = db.query(UserModel).all()
    return users

@router.get("/users/me")
def read_users_me(current_user: str = Depends(get_current_user)):
    return {"username": current_user}