from sqlalchemy import Column, Float, Integer, String, Text
from app.database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    color = Column(String)
    image_url = Column(String)
    name = Column(String)
    description = Column(Text)
