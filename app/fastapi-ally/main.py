from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from schemas.login import LoginRequest, LoginResponse
from schemas.user import UserInfo
from schemas.item import ItemCreate
from models.item import Item as DBItem

app = FastAPI()

# 假设的用户数据库
fake_user_db = {
    "alice": {
        "username": "alice",
        "password": "secret",
        "first_name": "Alice",
        "last_name": "Wonderland",
        "email": "alice@example.com"
    }
}

@app.post("/login", response_model=LoginResponse)
def login(request: LoginRequest):
    user_info = fake_user_db.get(request.username)
    if not user_info:
        return LoginResponse(code=404, data={}, msg="用户不存在")
    if user_info["password"] != request.password:
        return LoginResponse(code=400, data={}, msg="密码错误")
    return LoginResponse(code=200, data={"username": request.username}, msg="登录成功")

@app.get("/users/{username}", response_model=UserInfo)
def get_user(username: str):
    user_info = fake_user_db.get(username)
    if not user_info:
        raise HTTPException(status_code=404, detail="用户不存在")
    # 返回用户信息
    return UserInfo(
        username=user_info["username"],
        first_name=user_info["first_name"],
        last_name=user_info["last_name"],
        email=user_info["email"]
    )

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
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8888)
