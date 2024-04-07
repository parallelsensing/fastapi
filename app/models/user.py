from sqlalchemy import Column, Integer, String
from app.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    password = Column(String)
    phone = Column(String)

    def __repr__(self):
        return f"<User(username='{self.username}', first_name='{self.first_name}', last_name='{self.last_name}', phone='{self.phone}')>"
