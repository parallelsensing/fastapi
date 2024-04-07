from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from schemas.login import LoginRequest, LoginResponse
from schemas.user import UserInfo, UserCreate, UserResponse
from schemas.item import ItemCreate, ItemResponse
from models.item import Item as ItemModel
from models.user import User as UserModel
from typing import List

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

# return all users
@app.get("/users/", response_model=List[UserInfo])
def get_all_users(db: Session = Depends(get_db)) -> UserInfo:
    users = db.query(UserModel).all()
    return users

@app.post("/create_item", response_model=ItemCreate)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = ItemModel(
        latitude=item.coordinates[0],
        longitude=item.coordinates[1],
        color=item.color,
        image_url=item.image_url,
        name=item.name,
        description=item.description
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    # 手动构造响应数据
    return {
        "coordinates": (db_item.latitude, db_item.longitude),
        "color": db_item.color,
        "image_url": db_item.image_url,
        "name": db_item.name,
        "description": db_item.description
    }
    # return ItemResponse(code=200, msg="Item created successfully")

@app.get("/items/", response_model=List[ItemCreate])
def get_all_items(db: Session = Depends(get_db)):
    items = db.query(ItemModel).all()
    for item in items:
        item.coordinates = (item.latitude, item.longitude)
    return items

@app.get("/items/{item_id}", response_model=ItemCreate)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    item.coordinates = (item.latitude, item.longitude)
    return item

@app.post("/items/{search}", response_model=List[ItemCreate])
def search_item(search: str, db: Session = Depends(get_db)):
    items = db.query(ItemModel).filter(ItemModel.name.like(f"%{search}%")).all()
    for item in items:
        item.coordinates = (item.latitude, item.longitude)
    return items

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8888)
