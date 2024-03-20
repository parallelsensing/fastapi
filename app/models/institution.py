from sqlalchemy import Column, Integer, String
from app.db.base import Base, Common


class Institution(Base, Common):
  id = Column(Integer, primary_key=True, autoincrement=True)
  institution = Column(String(200), nullable=False)
  department = Column(String(200), nullable=False)
  address = Column(String(200), nullable=False)
  country = Column(String(200), nullable=False)
  province = Column(String(200), nullable=False)
  city = Column(String(200), nullable=False)
  postalCode = Column('postal_code', String(200), nullable=False)
  phone = Column(String(200), nullable=False)
  fax = Column(String(200), nullable=False)

  @classmethod
  def from_dict(cls, data):
    return cls(**data)
  