from sqlalchemy import Column, Float, Integer, String, Text
from app.core.database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    color = Column(String)
    image_url = Column(String)
    name = Column(String)
    description = Column(Text)
    image_name = Column(String)  # 添加新的图片名字字段
    image_time = Column(String)  # 添加新的图片时间字段
    placeholder = Column(String)  # 添加新的占位字段
