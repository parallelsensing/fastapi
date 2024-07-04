from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.schemas import LoginRequest, LoginResponse, UserInfo, UserCreate, UserResponse
from app.models import User as UserModel
from typing import List
from app.core.token import create_token, verify_token, get_current_user

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
    db_user = db.query(UserModel).filter(UserModel.username == user_data.username).first()
    if db_user:
        return UserResponse(code=400, msg="Username already registered")

    new_user = UserModel(
        username=user_data.username,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        password=user_data.password,
        phone=user_data.phone
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # 成功创建用户，构造响应
    return UserResponse(code=200, data=new_user.to_json(), msg="User created successfully")

@router.post("/login", response_model=LoginResponse)
def login(login_request: LoginRequest, db: Session = Depends(get_db)) -> LoginResponse:
    user = db.query(UserModel).filter(UserModel.phone == login_request.phone).first()
    

    if not user:
        return LoginResponse(code=404, msg="User not found", data={})

    if user.password != login_request.password:
        return LoginResponse(code=401, msg="Incorrect password", data={})
    
    token = create_token(user.username)

    # 假设登录成功
    return LoginResponse(code=200, msg="Login successful", data=user.to_json())


@router.get("/get_users/{username}", response_model=UserInfo)
def get_user(username: str, db: Session = Depends(get_db)) -> UserInfo:
    user = db.query(UserModel).filter(UserModel.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user  # 这里直接返回数据库模型实例

# return all users
@router.get("/get_users", response_model=List[UserInfo])
def get_all_users(db: Session = Depends(get_db)) -> UserInfo:
    users = db.query(UserModel).all()
    return users

@router.get("/users/me")
def read_users_me(current_user: str = Depends(get_current_user)):
    return {"username": current_user}