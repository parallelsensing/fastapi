from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.schemas import LoginRequest, LoginResponse, UserInfo, UserCreate, UserResponse,UserForgotPasswordRequest,UserResetPasswordRequest
from app.models import User as UserModel
from typing import List
from app.core.token import create_token, verify_token, get_current_user
from app.core.security import hash_password,verify_password
from app.utils import is_valid_email
# app = FastAPI()

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/create", response_model=UserResponse)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    if not is_valid_email(user_data.email):
        return UserResponse(code=400, msg="Invalid email address")
    db_user = db.query(UserModel).filter(UserModel.email == user_data.email).first()
    if db_user:
        return UserResponse(code=400, msg="Username already registered")
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

    
    # 假设登录成功
    # return LoginResponse(code=200, msg="Login successful", data={"token": token,"data":user.to_json()})
    return LoginResponse(code=200, msg="Login successful", data=user.to_json(),token=token)
@router.post("/reset_password",response_model=UserResponse)
def reset_password(resetBody:UserResetPasswordRequest, db: Session = Depends(get_db)):
    email:str = resetBody.email
    old_password:str = resetBody.old_password
    new_password:str = resetBody.new_password
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.password != old_password:
        raise HTTPException(status_code=401, detail="Incorrect password")
    user.password = new_password
    db.commit()
    db.refresh(user)
    return UserResponse(code=200, data=None, msg="Password reset successful")
@router.post("/forgot_password",response_model=UserResponse)
def forgot_password(forgotBody:UserForgotPasswordRequest, db: Session = Depends(get_db)):
    email:str = forgotBody.email
    new_password:str = forgotBody.new_password
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.password = new_password
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