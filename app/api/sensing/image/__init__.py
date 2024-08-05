from fastapi import FastAPI, Depends, HTTPException, APIRouter, File, UploadFile, Form,Request
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.schemas import ImageResponse, ImageMetadata,ImageListResponse,ImageDeletResponse
from app.models import Image as ImageModel
from typing import List
from app.core.token import create_token, verify_token, get_current_user
from app.core.config import settings
from app.core.llm import LLM,IncidentType
from app.utils import generate_unique_filename
import os
# app = FastAPI()
router = APIRouter()



# 确保文件保存目录存在
UPLOAD_DIR = settings.IMAGE_DIR
# print(UPLOAD_DIR)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@router.post("/upload", response_model=ImageResponse)
def upload_image(
    request: Request,
    file: UploadFile = File(...),
    image_name: str = Form(...),
    image_time: str = Form(...),
    placeholder: str = Form(""),
    db: Session = Depends(get_db),
    username: str = Depends(get_current_user)
):
    if not file:
        raise HTTPException(status_code=400, detail="No file part in the request")
    if not image_name:
        raise HTTPException(status_code=400, detail="Image name is required")
    if not image_time:
        raise HTTPException(status_code=400, detail="Image time is required")

    # 生成唯一文件名
    filename = generate_unique_filename(file.filename) 
    # 保存文件
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    
    # 调用大模型判断
    llm = LLM()
    llm.setPrompt("你是一个负责判断矿山安全事故类型的智能助手")
    data = llm.intelligentsJudgment(file_path)
    
    # 写入数据库
    image_url = str(request.url_for('images', path=filename))
    db_image = ImageModel(
        image_name=image_name,
        image_time=image_time,
        image_url=image_url,
        incident_type=data.type,
        placeholder=placeholder
    )
    
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    
    # print(data.type)
    return ImageResponse(
        message="File successfully uploaded",
        filename=file.filename,
        image_name=image_name,
        image_time=image_time,
        image_url=image_url,
        incident_type=data.type,
        placeholder=placeholder
    )

@router.get("/get_images" , response_model=List[ImageListResponse])
def get_images(
    db: Session = Depends(get_db),
    username: str = Depends(get_current_user)
):
    images = db.query(ImageModel).all()
    
    return images

@router.get("/get_image/{image_id}",response_model=ImageListResponse)
def get_image(image_id:int,db:Session = Depends(get_db),username: str = Depends(get_current_user)):
    image = db.query(ImageModel).filter_by(id=image_id).first()
    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return image

@router.get("/search/{image_name}",response_model=List[ImageMetadata])
def search_image(
    image_name:str,
    db:Session = Depends(get_db),
    username: str = Depends(get_current_user)
):
    images = db.query(ImageModel).filter(ImageModel.image_name.like(f"%{image_name}%")).all()
    if len(images) == 0:
        raise HTTPException(status_code=404, detail="Image not found")
    return images


@router.delete("/delete_image/{image_id}",response_model=ImageDeletResponse)
def delete_image(
    image_id:int,
    db:Session = Depends(get_db),
    username: str = Depends(get_current_user)
):
    image = db.query(ImageModel).filter_by(id=image_id).first()
    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    db.delete(image)
    db.commit()

    return image
