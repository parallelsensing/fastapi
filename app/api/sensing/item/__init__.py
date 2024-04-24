from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.schemas import ItemCreate, ItemCreate, ItemResponse
from app.models import Item as ItemModel
from app.models import User as UserModel
from typing import List
from core.token import get_current_user

# app = FastAPI()
router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create", response_model=ItemCreate)
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

@router.get("/get_items", response_model=List[ItemCreate])
def get_all_items(db: Session = Depends(get_db)):
    items = db.query(ItemModel).all()
    for item in items:
        item.coordinates = (item.latitude, item.longitude)
    return items

@router.get("/get_item_casia", response_model=ItemCreate)
def get_item_casia(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    # 根据current user的信息，获取user的权限，然后根据权限返回不同的数据
    user = db.query(UserModel).filter(UserModel.username == current_user).first()
    if user.role == 1:
        item = db.query(ItemModel).filter(ItemModel.name == "中国科学院自动化研究所").first()
        item.coordinates = (item.latitude, item.longitude)
        return item

@router.get("/get_items/{item_id}", response_model=ItemCreate)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    item.coordinates = (item.latitude, item.longitude)
    return item

@router.post("/items/{search}", response_model=List[ItemCreate])
def search_item(search: str, db: Session = Depends(get_db)):
    items = db.query(ItemModel).filter(ItemModel.name.like(f"%{search}%")).all()
    for item in items:
        item.coordinates = (item.latitude, item.longitude)
    return items