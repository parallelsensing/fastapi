from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from schemas.login import LoginRequest, LoginResponse
from schemas.user import UserInfo, UserCreate, UserResponse
from schemas.item import ItemCreate
from models.item import Item as DBItem
from models.user import User as UserModel

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/create_user", response_model=UserResponse)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    db_user = db.query(UserModel).filter(UserModel.username == user_data.username).first()
    if db_user:
        return UserResponse(code=400, msg="Username already registered")

    # 这里密码应进行加密处理，示例中直接使用明文
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
    return UserResponse(code=200, data=new_user, msg="User created successfully")

@app.post("/login", response_model=LoginResponse)
def login(login_request: LoginRequest, db: Session = Depends(get_db)) -> LoginResponse:
    user = db.query(UserModel).filter(UserModel.phone == login_request.phone).first()

    if not user:
        return LoginResponse(code=404, msg="User not found", data={})

    # 在这里添加密码验证逻辑，这里为了示例简单，假设密码是明文匹配
    # 实际应用应使用安全的密码哈希验证
    if user.password != login_request.password:
        return LoginResponse(code=401, msg="Incorrect password", data={})

    # 假设登录成功
    return LoginResponse(code=200, msg="Login successful", data=user)


@app.get("/users/{username}", response_model=UserInfo)
def get_user(username: str, db: Session = Depends(get_db)) -> UserInfo:
    user = db.query(UserModel).filter(UserModel.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user  # 这里直接返回数据库模型实例

# @app.post("/items/", response_model=ItemCreate)
# def create_item(item: ItemCreate, db: Session = Depends(get_db)):
#     db_item = DBItem(**item.dict())
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return item

@app.post("/items/", response_model=ItemCreate)
def create_item(item: ItemCreate):
    # 这里仅返回接收到的项目数据,暂时未连数据库
    return item

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8888)
