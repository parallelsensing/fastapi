from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.schemas import ItemCreate, ItemCreate, ItemResponse
from app.models import Item as ItemModel
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

@router.post("/create", response_model=ItemCreate)
def create_item(item: ItemCreate, db: Session = Depends(get_db), username: str = Depends(get_current_user)):
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
def get_all_items(db: Session = Depends(get_db), username: str = Depends(get_current_user)):
    items = db.query(ItemModel).all()
    for item in items:
        item.LngLat = (item.latitude, item.longitude)
    return items

@router.get("/get_items/{item_id}", response_model=ItemCreate)
def get_item(item_id: int, db: Session = Depends(get_db), username: str = Depends(get_current_user)):
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    item.LngLat = (item.latitude, item.longitude)
    return item

@router.post("/items/{search}", response_model=List[ItemCreate])
def search_item(search: str, db: Session = Depends(get_db), username: str = Depends(get_current_user)):
    items = db.query(ItemModel).filter(ItemModel.name.like(f"%{search}%")).all()
    if len(items) == 0:
        raise HTTPException(status_code=404, detail="Items not found")
    for item in items:
        item.LngLat = (item.latitude, item.longitude)
    return items
