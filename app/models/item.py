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

    def to_json(self)->dict:
        return {
            'id': self.id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone
        }