from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, sql, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped, column_property
from typing import TYPE_CHECKING
from app.db.base import Base, Common
if TYPE_CHECKING:
  from .author import Author  # noqa: F401


# class User(Base, Common):
#   """
#   User model
#   """
#   email = Column(String, unique=True, index=True, nullable=False)
#   password = Column(String, nullable=False)
#   isActive = Column("is_active", Boolean, default=True)
#   isAdmin = Column("is_admin", Boolean, default=False)
#   authorID = Column("author_id", Integer, ForeignKey("author.id", onupdate="CASCADE", ondelete="SET NULL"))
#   roleID = Column("role_id", Integer, ForeignKey("role.id", onupdate="CASCADE", ondelete="SET NULL"))

#   author:Mapped["Author"] = relationship("Author")

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

