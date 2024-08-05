from sqlalchemy import Column, Float, Integer, String, Text
from app.core.database import Base


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    image_name = Column(String)
    image_time = Column(String)
    image_url = Column(String)
    incident_type = Column(String)
    placeholder = Column(String)

    def to_json(self)->dict:
        return {
            'id': self.id,
            'image_name': self.image_name,
            'image_time': self.image_time,
            'image_url': self.image_url,
            'placeholder': self.placeholder
        }