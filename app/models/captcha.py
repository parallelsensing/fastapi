from sqlalchemy import Column, Float, Integer, String, Text,TIMESTAMP
from app.core.database import Base
from sqlalchemy.sql import func

class CaptchaModel(Base):
    __tablename__ = "captchas"

    id = Column(Integer, primary_key=True, index=True) # Primary key, indexed
    code = Column(String) # 验证码
    email = Column(String) # 邮箱
    timestamp = Column(TIMESTAMP, server_default=func.now(), nullable=False)  # 时间戳
    def to_json(self)->dict:
        return {
            'id': self.id,
            'code': self.code,
            'email': self.email,
            'timestamp': self.timestamp
        }